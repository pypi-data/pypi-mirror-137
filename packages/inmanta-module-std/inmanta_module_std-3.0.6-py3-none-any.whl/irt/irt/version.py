"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import configparser
import enum
import json
import logging
import os
import subprocess
import sys
from abc import ABC, abstractmethod
from enum import Enum
from functools import total_ordering
from typing import Dict, List, Optional

from packaging.version import Version

from irt import util

LOGGER = logging.getLogger(__name__)


@total_ordering
@enum.unique
class ChangeType(Enum):
    MAJOR: str = "major"
    MINOR: str = "minor"
    PATCH: str = "patch"

    def less(self) -> Optional["ChangeType"]:
        """
        Returns the change type that is one less than this one.
        """
        if self == ChangeType.MAJOR:
            return ChangeType.MINOR
        if self == ChangeType.MINOR:
            return ChangeType.PATCH
        return None

    def __lt__(self, other: "ChangeType") -> bool:
        order: List[ChangeType] = [ChangeType.PATCH, ChangeType.MINOR, ChangeType.MAJOR]
        if other not in order:
            return NotImplemented
        return order.index(self) < order.index(other)

    @classmethod
    def diff(cls, *, low: Version, high: Version) -> Optional["ChangeType"]:
        """
        Returns the order of magnitude of the change type diff between two versions. Returns None if there is no diff.
        """
        if low > high:
            raise ValueError(f"Expected low <= high, got {low} > {high}")
        if Version(low.base_version) != low:
            raise ValueError(
                f"{cls.__name__}.diff only supports stable versions, got {low}"
            )
        if Version(high.base_version) != high:
            raise ValueError(
                f"{cls.__name__}.diff only supports stable versions, got {high}"
            )
        if low == high:
            return None
        if high.major > low.major:
            return cls.MAJOR
        if high.minor > low.minor:
            return cls.MINOR
        if high.micro > low.micro:
            return cls.PATCH
        raise Exception(
            "Couldn't determine version change type diff: this state should be unreachable"
        )


class VersionBumpTool(ABC):
    def __init__(self, project_path: str) -> None:
        self.project_path: str = project_path

    @classmethod
    def requires_file(cls) -> Optional[str]:
        return None

    @abstractmethod
    def get_version(self) -> Version:
        raise NotImplementedError()

    @abstractmethod
    def bump(self, change_type: ChangeType) -> None:
        raise NotImplementedError()

    @abstractmethod
    def set_version(self, version: Version) -> None:
        raise NotImplementedError()


class Bumpversion(VersionBumpTool):
    @classmethod
    def requires_file(cls) -> str:
        return ".bumpversion.cfg"

    def get_version(self) -> Version:
        parser: configparser.ConfigParser = configparser.ConfigParser()
        parser.read(os.path.join(self.project_path, ".bumpversion.cfg"))
        version: str
        try:
            version = parser.get("bumpversion", "current_version")
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            raise Exception("failed to determine project version") from e
        else:
            return Version(version)

    def bump(self, change_type: ChangeType) -> None:
        util.subprocess_log(
            subprocess.check_output,
            [
                sys.executable,
                "-m",
                "bumpversion",
                "--allow-dirty",
                "--no-commit",
                "--no-tag",
                change_type.value,
            ],
            logger=LOGGER,
            cwd=self.project_path,
        )

    def set_version(self, version: Version) -> None:
        if self.get_version() == version:
            # circumvent a bug in bumpversion (c4urself/bump2version#214)
            return
        util.subprocess_log(
            subprocess.check_output,
            [
                sys.executable,
                "-m",
                "bumpversion",
                "--allow-dirty",
                "--no-commit",
                "--no-tag",
                "--new-version",
                str(version),
                "none",
            ],
            logger=LOGGER,
            cwd=self.project_path,
        )


class Yarn(VersionBumpTool):
    @classmethod
    def requires_file(cls) -> str:
        return "package.json"

    def get_version(self) -> Version:
        text: str
        with open(os.path.join(self.project_path, "package.json"), "r") as f:
            text = f.read()
        data: Dict = json.loads(text)
        version: str
        try:
            version = data["version"]
        except KeyError as e:
            raise Exception("Failed to determine project version") from e
        else:
            return Version(version)

    def bump(self, change_type: ChangeType) -> None:
        util.subprocess_log(
            subprocess.check_output,
            [
                "yarn",
                "version",
                f"--{change_type.value}",
                "--no-git-tag-version",
            ],
            logger=LOGGER,
            cwd=self.project_path,
        )

    def set_version(self, version: Version) -> None:
        util.subprocess_log(
            subprocess.check_output,
            [
                "yarn",
                "version",
                "--new-version",
                str(version),
                "--no-git-tag-version",
            ],
            logger=LOGGER,
            cwd=self.project_path,
        )
