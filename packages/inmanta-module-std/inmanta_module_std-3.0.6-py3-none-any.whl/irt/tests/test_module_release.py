"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import os
import shutil
import subprocess
import tempfile
from typing import List

from irt import git
from irt.release import modules


def create_empty_git_repo(repo_path: str, create_master_branch: bool = False) -> str:
    subprocess.check_call(["git", "init", "--bare", repo_path])
    repo_url = f"file://{repo_path}"
    if create_master_branch:
        ensure_master_branch(repo_url)
    return repo_url


def ensure_master_branch(git_repo_url: str) -> None:
    with tempfile.TemporaryDirectory() as clone_dir:
        subprocess.check_call(["git", "clone", git_repo_url, clone_dir])
        file_in_repo = os.path.join(clone_dir, "README")
        add_file(file_in_repo, "test")
        subprocess.check_call(["git", "add", file_in_repo], cwd=clone_dir)
        subprocess.check_call(["git", "commit", "-m", "initial commit"], cwd=clone_dir)
        subprocess.check_call(["git", "push", "origin", "master"], cwd=clone_dir)


def add_file(path: str, content: str) -> None:
    with open(path, "w") as f:
        f.write(content)


def apply_change_to_repo_and_add_tag(
    branch: git.Branch, file_name: str, content: str, tag_name: str
) -> None:
    file_path = os.path.join(branch.repo.directory, file_name)
    add_file(file_path, content)
    branch.commit(f"Updated {file_path}")
    branch.push()
    branch.add_annotated_tag(tag_name, message=f"Adding tag {tag_name}", push=True)


def get_remote_tags(git_repo_url: str) -> List[str]:
    output = subprocess.check_output(
        ["git", "ls-remote", "--tags", "--refs", git_repo_url]
    )
    return [
        t.split("\t")[1].split("/")[-1]
        for t in output.decode("utf-8").split("\n")
        if t.strip()
    ]


def test_module_release(tmpdir):
    # Create two empty git repositories
    upstream_repo_path = os.path.join(tmpdir, "upstream_repo")
    upstream_repo_url = create_empty_git_repo(
        upstream_repo_path, create_master_branch=True
    )
    customer_facing_repo1_path = os.path.join(tmpdir, "customer_facing_repo1")
    customer_facing_repo1_url = create_empty_git_repo(
        customer_facing_repo1_path, create_master_branch=False
    )

    upstream_clone_dir = os.path.join(tmpdir, "upstream_clone_dir")
    upstream_clone_git_repo = git.GitRepo(
        url=upstream_repo_url, clone_dir=upstream_clone_dir
    )

    # Populate upstream repo
    with upstream_clone_git_repo.checkout_branch(branch="master") as branch:
        apply_change_to_repo_and_add_tag(
            branch=branch, file_name="test", content="change1", tag_name="1.0.0"
        )

    with upstream_clone_git_repo.checkout_branch(
        branch="other-branch", base_branch="master"
    ) as branch:
        apply_change_to_repo_and_add_tag(
            branch=branch, file_name="test", content="change2", tag_name="1.0.1"
        )

    with upstream_clone_git_repo.checkout_branch(branch="master") as branch:
        apply_change_to_repo_and_add_tag(
            branch=branch, file_name="test", content="change3", tag_name="1.1.0"
        )
        apply_change_to_repo_and_add_tag(
            branch=branch, file_name="test", content="change4", tag_name="1.2.0"
        )
        apply_change_to_repo_and_add_tag(
            branch=branch, file_name="test", content="change5", tag_name="1.3.0"
        )

    expected_tags_upstream = ["1.0.0", "1.0.1", "1.1.0", "1.2.0", "1.3.0"]
    expected_tags_customer_facing = []

    # Perform release from latest version 1.2.0
    with upstream_clone_git_repo.checkout_branch(branch="1.2.0"):
        assert get_remote_tags(upstream_repo_url) == expected_tags_upstream
        assert (
            get_remote_tags(customer_facing_repo1_url) == expected_tags_customer_facing
        )
        modules.release_module(
            module_name="test",
            module_path=upstream_clone_dir,
            push_url=customer_facing_repo1_url,
        )
        # Ensure that tag 1.0.1 and 1.3.0 are not pushed
        expected_tags_customer_facing = ["1.0.0", "1.1.0", "1.2.0"]
        assert get_remote_tags(upstream_repo_url) == expected_tags_upstream
        assert (
            get_remote_tags(customer_facing_repo1_url) == expected_tags_customer_facing
        )

    # Remove upstream_clone_dir because modules.release_module() changes the remote
    shutil.rmtree(upstream_clone_dir)
    upstream_clone_git_repo = git.GitRepo(
        url=upstream_repo_url, clone_dir=upstream_clone_dir
    )

    # Add extra tag 2.0.0 + release from master
    with upstream_clone_git_repo.checkout_branch(branch="master") as branch:
        apply_change_to_repo_and_add_tag(
            branch=branch, file_name="test", content="change6", tag_name="2.0.0"
        )

        expected_tags_upstream.append("2.0.0")
        assert get_remote_tags(upstream_repo_url) == expected_tags_upstream
        assert (
            get_remote_tags(customer_facing_repo1_url) == expected_tags_customer_facing
        )
        modules.release_module(
            module_name="test",
            module_path=upstream_clone_dir,
            push_url=customer_facing_repo1_url,
        )
        # Ensure 1.3.0 and 2.0.0 are pushed
        expected_tags_customer_facing.extend(["1.3.0", "2.0.0"])
        assert get_remote_tags(upstream_repo_url) == expected_tags_upstream
        assert (
            get_remote_tags(customer_facing_repo1_url) == expected_tags_customer_facing
        )

    # Remove upstream_clone_dir because modules.release_module() changes the remote
    shutil.rmtree(upstream_clone_dir)
    upstream_clone_git_repo = git.GitRepo(
        url=upstream_repo_url, clone_dir=upstream_clone_dir
    )

    # Release other-branch to customer_facing_repo2
    expected_tags_customer_facing = []
    customer_facing_repo2_path = os.path.join(tmpdir, "customer_facing_repo2")
    customer_facing_repo2_url = create_empty_git_repo(
        customer_facing_repo2_path, create_master_branch=False
    )
    with upstream_clone_git_repo.checkout_branch(branch="other-branch"):
        assert get_remote_tags(upstream_repo_url) == expected_tags_upstream
        assert (
            get_remote_tags(customer_facing_repo2_url) == expected_tags_customer_facing
        )
        modules.release_module(
            module_name="test",
            module_path=upstream_clone_dir,
            push_url=customer_facing_repo2_url,
        )
        # Ensure only "1.0.0" and 1.0.1 are pushed
        expected_tags_customer_facing = ["1.0.0", "1.0.1"]
        assert get_remote_tags(upstream_repo_url) == expected_tags_upstream
        assert (
            get_remote_tags(customer_facing_repo2_url) == expected_tags_customer_facing
        )
