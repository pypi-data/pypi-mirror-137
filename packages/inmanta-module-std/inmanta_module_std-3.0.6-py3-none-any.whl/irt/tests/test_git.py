"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import os
import subprocess
import uuid
from pathlib import Path

import pytest

from irt.git import git_repo

try:
    token = os.environ["GITHUB_TOKEN"]
except Exception:
    raise Exception(
        "The GITHUB_TOKEN environment variable must be set to run these tests"
    )


def test_git_repo_context_manager(dummy_product_repo: str) -> None:
    with git_repo(dummy_product_repo, token) as repo:
        assert os.path.isdir(repo.directory)
        out: str = subprocess.check_output(
            ["git", "remote", "get-url", "origin"], cwd=repo.directory
        ).decode()
        assert (
            out.strip()
            == f"https://{token}@github.com/inmanta/dummy-inmanta-product.git"
        )


def test_checkout_branch(dummy_product_repo: str) -> None:
    with git_repo(dummy_product_repo, token) as repo:
        with repo.checkout_branch("dummy-next"):
            out: str = subprocess.check_output(
                ["git", "branch", "--show-current"], cwd=repo.directory
            ).decode()
            assert out.strip() == "dummy-next"
            touch_file: str = os.path.join(repo.directory, "touch_file")
            Path(touch_file).touch()
            assert os.path.isfile(touch_file)
        assert not os.path.isfile(touch_file)


def test_checkout_branch_nested(dummy_product_repo: str) -> None:
    with pytest.raises(
        Exception, match="Can not enter context: already in a `with` block"
    ):
        with git_repo(dummy_product_repo, token) as repo:
            with repo.checkout_branch("dummy-next"):
                with repo.checkout_branch("master"):
                    assert repo.get_commit()


def test_checkout_new_branch(dummy_product_repo: str) -> None:
    with git_repo(dummy_product_repo, token) as repo:
        with repo.checkout_branch("dummy-next"):
            # check out other branch first so we're sure new branch is not just branched off current branch
            pass
        with repo.checkout_branch("my-new-branch", base_branch="master"):
            out: str = subprocess.check_output(
                ["git", "branch", "--show-current"], cwd=repo.directory
            ).decode()
            assert out.strip() == "my-new-branch"
            assert repo.get_branch_head("my-new-branch") == repo.get_branch_head(
                "master"
            )


def test_list_branches(dummy_product_repo: str) -> None:
    with git_repo(dummy_product_repo, token) as repo:
        assert set(repo.get_all_branches()).issuperset({"master", "iso4", "iso3"})
        new_branch: str = str(uuid.uuid4())
        with repo.checkout_branch(new_branch, base_branch="master"):
            pass
        assert set(repo.get_all_branches()).issuperset(
            {new_branch, "master", "iso4", "iso3"}
        )


def test_commit(dummy_product_repo: str) -> None:
    with git_repo(dummy_product_repo, token) as repo:
        hello: str = "Hello World!"
        head: str = repo.get_branch_head("master")
        with repo.checkout_branch("master") as branch:
            with open(os.path.join(repo.directory, "myfile"), "w") as f:
                f.write(hello)
            branch.commit("Hello World")
            new_head: str = repo.get_branch_head(branch.branch)
            assert new_head != head
            with pytest.raises(Exception):
                branch.commit("Empty commit")
            branch.commit("Empty commit", ignore_empty=True)
            assert repo.get_branch_head(branch.branch) == new_head

        with repo.checkout_branch("master") as branch:
            with open(os.path.join(repo.directory, "myfile"), "r") as f:
                assert f.read().strip() == hello
