"""A small and simple wrapper for GitPython for GitLab repos."""

import sys

import git

from .script_helpers import error
from .utils import right_replace


def _get_git_repo():
    """:return: a ``git.Repo`` instance."""
    try:
        return git.Repo(search_parent_directories=True)
    except git.exc.InvalidGitRepositoryError as exc:
        error(f"No git repo found: {exc!s}")
        sys.exit(1)


def _get_remote_url():
    """Return the remote from local git repo"""
    repo = _get_git_repo()

    if not repo.remotes:
        error("There are no remotes for this repo. Use --server.")
        sys.exit(1)

    remote = repo.remotes[0]

    if remote.name != "origin":
        for remo in repo.remotes:
            if remo.name == "origin":
                remote = remo

    return remote.url


def get_server_url():
    """
    Return a url to the gitlab server which is the remote of the current repo
    """
    url = _get_remote_url()

    if url.startswith("https://"):
        # https
        url = url.replace("https://", "", 1).split("/")[0]
    elif "@" in url and ":" in url:
        # ssh
        url = "https://{0}/".format(url.split("@")[1].split(":")[0])
    else:
        error(f"The remotes url/protocol is not supported: {url}")

    return url


def get_project_name():
    """
    Return the name of the current repository on the remote gitlab server
    includeing the user/group name (e.g.: 'foogroup/foorepo')
    """
    url = _get_remote_url()

    if url.endswith(".git"):
        url = right_replace(url, ".git", "", 1)

    if "@" in url and ":" in url:
        # ssh
        project = url.split(":", 1)[1]
    elif url.startswith("https://"):
        # https
        project = "/".join(url.replace("https://", "", 1).split("/")[1:])
    else:
        error(f"Unknown repo URL format: {url!s}")
        sys.exit(2)

    return project


def get_shas():
    """Return list of all commits in current repo"""
    repo = _get_git_repo()

    return [ci.hexsha for ci in repo.iter_commits()]


def get_long_commit_sha(hexsha):
    """Return the long hexsha for the commit with sha hexsha"""
    repo = _get_git_repo()

    for commit in repo.iter_commits():
        if commit.hexsha.startswith(hexsha):
            return commit.hexsha

    return None


def get_current_commit():
    """Return the commit hash of the current working copy"""
    repo = _get_git_repo()

    return repo.head.commit.hexsha
