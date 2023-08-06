"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import logging
import os
import subprocess
import tempfile
from typing import List, Optional, Set

from packaging.version import Version
from pkg_resources import Requirement

import irt.module_sources
from inmanta.module import InmantaModuleRequirement, ModuleV2Source
from irt import util
from irt.const import COMPILED_SEMVER_REGEX_STABLE_VERSION
from irt.credentials import CredentialName, CredentialStore
from irt.modules import (
    ModuleSetDefinition,
    download_module_set_for_product,
    install_product,
)
from irt.release import BuildType
from irt.release.build import Cloudsmith, Devpi

LOGGER = logging.getLogger(__name__)


def push_module_set(
    product_repo: str,
    branch: str,
    working_dir: str,
    github_token: str,
    dry_run: bool,
    sources: irt.module_sources.ModuleSourceManager,
    push_single_module: Optional[str] = None,
) -> None:

    product_config, python_path = install_product(
        branch, github_token, product_repo, BuildType.stable, working_dir
    )

    if product_config.module_set.publish_repo is None:
        raise Exception("tool.irt.module_set.publish_repo is not set in pyproject.toml")

    module_set, modules_dir, set_def = download_module_set_for_product(
        python_path, working_dir, product_config, sources, github_token
    )

    LOGGER.info("Pushing releases for module set %s", set_def.name)
    remote = product_config.module_set.publish_repo.rstrip("/")
    modules_to_release = (
        [push_single_module]
        if push_single_module is not None
        else list(module_set.keys())
    )
    for module_name in modules_to_release:
        LOGGER.info("Releasing module: %s", module_name)
        module_path = os.path.join(modules_dir, module_name)
        push_url = f"{remote}/{module_name}.git"
        release_module(module_name, module_path, push_url, dry_run=dry_run)


def release_module(
    module_name: str, module_path: str, push_url: str, dry_run: bool = False
) -> None:
    _add_upstream(module_path, "origin", push_url)
    tags = _get_tags(module_path, push_url)
    if dry_run:
        LOGGER.info(
            "The following tags would be pushed for module %s: %s", module_name, tags
        )
    else:
        _push_tags(module_path, "origin", tags)


def _add_upstream(module_path: str, remote_name: str, remote: str) -> None:
    try:
        cmd = ["git", "remote", "remove", remote_name]
        util.subprocess_log(subprocess.check_call, cmd, logger=LOGGER, cwd=module_path)
    except subprocess.CalledProcessError:
        pass

    cmd = ["git", "remote", "add", remote_name, remote]
    util.subprocess_log(subprocess.check_call, cmd, logger=LOGGER, cwd=module_path)


def _get_tags(module_path: str, remote: str) -> List[str]:
    LOGGER.debug("collecting tags")
    # Calculate all tags that should be present on remote after the release
    tags_required_by_remote = (
        util.subprocess_log(
            subprocess.check_output,
            ["git", "tag", "--merged"],
            logger=LOGGER,
            stderr=subprocess.DEVNULL,
            cwd=module_path,
        )
        .decode()
        .splitlines()
    )

    # Calculate tags released in previous release
    raw_tags = (
        util.subprocess_log(
            subprocess.check_output,
            ["git", "ls-remote", "--tags", "--refs", remote],
            logger=LOGGER,
        )
        .decode()
        .splitlines()
    )
    already_released_tags = []
    for line in raw_tags:
        already_released_tags.append(line.split("\t")[1].replace("refs/tags/", ""))

    # Calculate diff between tags_required_by_remote and already_released_tags
    tags_to_push = []
    for tag in tags_required_by_remote:
        if (
            COMPILED_SEMVER_REGEX_STABLE_VERSION.match(tag)
            and tag not in already_released_tags
        ):
            tags_to_push.append(tag)

    return tags_to_push


def _push_tags(module_path: str, remote_name: str, tags: List[str]) -> None:
    if tags:
        LOGGER.debug(f"pushing tags: {tags}")
        checkout_latest_tag_cmd = ["git", "checkout", tags[-1]]
        util.subprocess_log(
            subprocess.check_call,
            checkout_latest_tag_cmd,
            logger=LOGGER,
            cwd=module_path,
        )

        push_to_master_cmd = [
            "git",
            "push",
            "--force",
            remote_name,
            "HEAD:refs/heads/master",
        ]
        util.subprocess_log(
            subprocess.check_call, push_to_master_cmd, logger=LOGGER, cwd=module_path
        )

        # Push all tags at once
        push_tags_cmd = ["git", "push", remote_name] + tags
        util.subprocess_log(
            subprocess.check_call, push_tags_cmd, logger=LOGGER, cwd=module_path
        )
    else:
        LOGGER.debug("remote already up to date")


def publish_modules_to_external_repository(
    modules_to_release: List[str],
    source_repository: str,
    module_set_definition: ModuleSetDefinition,
    credentials: CredentialStore,
    dry_run: bool,
    push_specific_version: Optional[str] = None,
) -> None:
    """
    Publish the given list of modules from the given source Python package repository
    to the publish_repo configured in the module set file. All module version will be
    pushed that match the version constraint defined in the `module` section of the
    module set file.

    :param modules_to_release: A list of module names (not the Python package name).
    :param dry_run: Only report which version of which modules would be pushed.
    :param push_specific_version: Only push packages with this specific version number.
    """
    # Source repo
    devpi = Devpi(url=source_repository)
    # Destination repo
    cloudsmith_api_key = credentials.get_credentials_for(
        CredentialName.CLOUDSMITH_API_KEY, allow_unset=False
    )
    # Make mypy happy
    assert cloudsmith_api_key is not None
    if module_set_definition.publish_repo is None:
        raise Exception("No `publish_repo` was defined in the module set file.")
    cloudsmith = Cloudsmith(
        module_set_definition.publish_repo, cloudsmith_api_key.password
    )
    for module_name in modules_to_release:
        version_constraint_module_set_file: Requirement = (
            ModuleV2Source.get_python_package_requirement(
                module_set_definition.get_version_constraint_for(module_name)
            )
        )
        version_constraint: Requirement
        if push_specific_version:
            version_constraint = ModuleV2Source.get_python_package_requirement(
                InmantaModuleRequirement.parse(
                    f"{module_name}=={push_specific_version}"
                )
            )
            if push_specific_version not in version_constraint_module_set_file:
                raise Exception(
                    f"Requested to push {version_constraint}, but this version conflicts with "
                    f"the version constraint defined in the module set file {version_constraint_module_set_file}."
                )
        else:
            version_constraint = version_constraint_module_set_file

        devpi_versions: Set[Version] = devpi.get_versions_for_package(
            version_constraint.key, version_constraint, allow_prereleases=False
        )
        cloudsmith_versions: Set[Version] = cloudsmith.get_versions_for_package(
            version_constraint.key, version_constraint, allow_prereleases=False
        )
        versions_to_publish: List[Version] = sorted(
            [ver for ver in devpi_versions - cloudsmith_versions]
        )
        # Logging
        if versions_to_publish:
            LOGGER.info(
                "The following version of %s will be published: %s",
                module_name,
                [str(ver) for ver in versions_to_publish],
            )
        else:
            LOGGER.info(
                "No new releases for module %s that match the version constraint %s: skipping",
                module_name,
                str(version_constraint),
            )
        if dry_run:
            continue
        # Publish packages
        for version in versions_to_publish:
            with tempfile.TemporaryDirectory() as work_dir:
                path_to_pkg = devpi.download_universal_wheel(
                    version_constraint.key, version, work_dir
                )
                cloudsmith.publish_python_package(path_to_pkg)
