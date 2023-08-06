#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

"""Command line interface for GitLab CI."""

import argparse
import os
import sys
import typing
from dataclasses import dataclass
from functools import cached_property
from getpass import getpass
from pathlib import Path

import keyring
from tabulate import tabulate
from termcolor import colored, cprint

import gitlabcicli as info
from gitlabcicli.gitlabapiwrapper import GitLabApiClient
from gitlabcicli.gitwrapper import (
    get_current_commit,
    get_long_commit_sha,
    get_project_name,
    get_server_url,
    get_shas,
)
from gitlabcicli.script_helpers import debug, error, set_verbosity

try:
    import argcomplete
except ImportError:
    argcomplete = None

KNOWN_STATES = {
    "unknown": {
        "color": "yellow",
        "severity": 0,
    },
    "success": {
        "color": "green",
        "severity": 1,
    },
    "pending": {
        "color": "magenta",
        "severity": 2,
    },
    "running": {
        "color": "blue",
        "severity": 3,
    },
    "canceled": {
        "color": "grey",
        "severity": 4,
    },
    "failed": {
        "color": "red",
        "severity": 5,
    },
    "failed (allowed)": {
        "color": "yellow",
        "severity": 2,
    },
    "created": {
        "color": "yellow",
        "severity": 2,
    },
    "skipped": {"color": "blue", "severity": 2},
    "manual": {"color": "red", "severity": 4},
}


@dataclass
class Command:
    """A cmd command."""

    name: str
    aliases: frozenset[str]
    doc: str


COMMANDS = dict[str, Command]()


def register_command(
    *,
    name: typing.Optional[str] = None,
    aliases: set[str] = frozenset[str](),
    doc: typing.Optional[str] = None,
) -> typing.Callable:
    """Decorator to register a command"""

    def inner(func: typing.Callable) -> typing.Callable:
        cmd_name = name or func.__name__.replace("_", "-")
        COMMANDS[cmd_name] = Command(
            name=cmd_name,
            aliases=frozenset(aliases),
            doc=doc or func.__doc__,
        )

        return func

    return inner


KEYRING_SERVICE_NAME = "gitlabcicli"


def sha_completer(prefix, **kwargs):
    """tab completion shas in current git"""

    return (s[:8] for s in get_shas() if s.startswith(prefix))


def gitlabciyml_completer(prefix, **_):
    """tab completion for .gitlab-ci.yml"""
    files = argcomplete.completers.FilesCompleter()(prefix)
    print(files)

    return [
        fn
        for fn in files
        if (os.path.isdir(fn) or ".gitlab-ci.yml".startswith(fn.split("/")[-1]))
    ]


def get_token_from_keyring(server_url: str) -> typing.Optional[str]:
    """Retreive the token for current server from keyring."""

    try:
        return keyring.get_password(KEYRING_SERVICE_NAME, server_url)
    except Exception as exc:
        error(
            "No token found in wallet. Please use --ask-for-token to specify your token."
        )
        error(str(exc))
        sys.exit(500)

    return None


def _color_job_status(status):
    """Return the colored job status as string"""

    return colored(status, attrs=["bold"], color=KNOWN_STATES[status]["color"])


def _color_coverage(coverage):
    """Return the colored coverage as string"""

    if coverage:
        color = "red"

        if coverage > 90:
            color = "green"
        elif coverage > 75:
            color = "yellow"

        return colored(f"{coverage:.1f}%", color=color)
    else:
        debug("No coverage found", min_debug_level=5)

        return ""


def print_job_table(jobs):
    """Print information about the jobs to stdout."""
    pipeline_url = jobs[0]["pipeline"]["web_url"]
    commit_hash = jobs[0]["commit"]["short_id"]
    commit_ref = jobs[0]["ref"]
    commit_title = jobs[0]["commit"]["title"]
    commit_author = jobs[0]["commit"]["author_name"]
    assert all(job["commit"]["short_id"] == commit_hash for job in jobs)
    assert all(job["ref"] == commit_ref for job in jobs)
    assert all(job["commit"]["title"] == commit_title for job in jobs)
    assert all(job["commit"]["author_name"] == commit_author for job in jobs)
    assert all(job["pipeline"]["web_url"] == pipeline_url for job in jobs)
    commit_hash = colored(commit_hash, color="grey")
    commit_ref = colored(commit_ref, color="blue")
    commit_title = colored(commit_title, attrs=["bold"])
    commit_author = colored(commit_author, color="cyan")
    pipeline_url = colored(pipeline_url, attrs=["underline"])
    print(
        f"Commit: {commit_hash} (Ref: {commit_ref}) - {commit_title} - {commit_author}"
    )
    print()
    print(f"Pipeline URL: {pipeline_url}")
    print()

    table_jobs = []
    table_headers = [
        "id",
        "status",
        "stage",
        "name",
        "duration",
        "coverage",
    ]

    def format_duration(duration: float):
        if not duration:
            return ""

        minute = 60
        hour = 60 * minute
        day = 24 * hour
        days, duration = divmod(duration, day)
        hours, duration = divmod(duration, hour)
        minutes, duration = divmod(duration, minute)
        seconds = round(duration)
        ret = ""

        if days:
            ret += f"{days:.0f} days "

        if hours:
            ret += f"{hours:.0f} h "

        if minutes:
            ret += f"{minutes:.0f} min "

        if seconds:
            ret += f"{seconds:.0f} s"

        return ret.strip()

    for job in jobs:
        debug(job["status"], 5)

        if job["status"] not in KNOWN_STATES.keys():
            error(f'[!] Status "{job["status"]}" is unknown!')

            continue
        job_status = job["status"]

        if job_status == "failed" and job.get("allow_failure"):
            job_status = "failed (allowed)"
        table_job = [
            job["id"],
            _color_job_status(job_status),
            job["stage"],
            job["name"],
            format_duration(job.get("duration", 0)),
            _color_coverage(job["coverage"]),
        ]
        table_jobs.append(table_job)
    print(tabulate(table_jobs, headers=table_headers, disable_numparse=True))


class GitLabCiCli(object):
    """A Cli class."""

    def __init__(self, **kwargs):
        self._api_client: typing.Optional[GitLabApiClient] = None
        self._server_url: typing.Optional[str] = kwargs.get("server_url", None)
        self._project_id: typing.Optional[int] = kwargs.get("project_id", None)
        self._project_path: typing.Optional[str] = kwargs.get("project_path", None)
        self._project: typing.Optional[str] = kwargs.get("project", None)
        self._token: typing.Optional[str] = kwargs.get("token", None)
        self._commit_hash: typing.Optional[str] = kwargs.get("commit_hash", None)
        self.args = kwargs

    def stop(self):
        """Shutdown."""

        if self._token:
            keyring.set_password(KEYRING_SERVICE_NAME, self.server_url, self._token)

    @property
    def server_url(self) -> str:
        if not self._server_url:
            debug("Try to get server url from remote of local git repo...", 2)
            self._server_url = get_server_url()
            debug(f"Using server {self._server_url}", 1)

        assert self._server_url

        return self._server_url

    @property
    def api_client(self) -> GitLabApiClient:
        if not self._api_client:
            assert self.token
            self._api_client = GitLabApiClient(
                server_url=self.server_url, token=self.token
            )

        return self._api_client

    @property
    def project_id(self) -> int:
        if self._project_id is None:
            self._project_id = self.api_client.get_project_id(self.project)

            if self._project_id == -1:
                error("Could not determine the project ID.")

        assert self._project_id is not None

        return self._project_id

    @property
    def project_path(self) -> str:
        if not self._project_path:
            self._project_path = self.api_client.get_project_path(self.project_id)

            if not self._project_path:
                error("Could not determine the project path.")

        return self._project_path

    @property
    def commit_hash(self) -> str:
        if not self._commit_hash:
            # ref is better than commit
            debug("Try to get commit from remote of local git repo...", 2)
            self._commit_hash = get_current_commit()
            debug(f"Using commit {self._commit_hash}", 1)

        assert self._commit_hash

        return self._commit_hash

    @property
    def project(self) -> str:
        if not self._project:
            debug("Try to get project from remote of local git repo...", 2)
            self._project = get_project_name()
            debug(f"Using project {self._project}", 1)

        assert self._project

        return self._project

    @cached_property
    def token(self) -> str:
        """The secret API token."""

        if self.args.get("ask_for_token"):
            debug("Try to get token from user input...", 2)
            self._token = getpass(
                f"Please enter the GitLab API Token for {self.server_url}: "
            )
        elif not self._token:
            debug("Try to get token for server from config...", 2)
            self._token = get_token_from_keyring(self.server_url)

        if not self._token:
            error(
                "No token found in wallet or given. Please use --ask-for-token to specify your token."
            )
            sys.exit(501)

        debug(f"Using token {self._token}", 5)

        return self._token

    def get_jobs(self):
        """Return a list of jobs to handle."""

        if "job_ids" in self.args and self.args["job_ids"]:
            jobs = []

            for jid in self.args["job_ids"]:
                job = self.api_client.get_job_for_id(
                    project_id=self.project_id,
                    job_id=jid,
                )

                if job:
                    jobs.append(job)
        else:
            pipeline_id = self.api_client.get_pipeline_for_commit(
                project_id=self.project_id,
                commit_hash=self.commit_hash,
            )

            if not pipeline_id:
                error(f"No pipeline found for commit {self.commit_hash}")
                exit(404)
            jobs = self.api_client.get_pipeline_jobs(
                project_id=self.project_id,
                pipeline_id=pipeline_id,
            )
            jobs = sorted(jobs, key=lambda v: v["id"])

        return jobs

    @register_command(aliases={"status"})
    def show(self):
        """Run gitlabcicli show."""
        jobs = self.get_jobs()

        if not jobs:
            error("No jobs found.")

            return
        print_job_table(jobs)

    @register_command(aliases={"log"})
    def raw(self):
        """run gitlabcicli raw"""
        jobs = self.get_jobs()

        for job in jobs:
            artifacts = job.get("artifacts", [])
            traces = [
                artifact
                for artifact in artifacts
                if artifact.get("file_type") == "trace"
            ]
            job_id = job.get("id")

            if not traces:
                error(
                    f"There is no job log yet for job #{job_id} for project '{self.project}'."
                )

                continue
            elif len(traces) > 1:
                error(
                    f"There are too many job logs for job #{job_id} for project '{self.project}'."
                )

                continue

            trace_file_name = traces.pop().get("filename")
            print()
            cprint(f" === Job output of job #{job['id']} === ", attrs=["bold"])
            print()
            raw_output = self.api_client.get_job_artifact(
                project_path=self.project_path,
                job_id=job["id"],
                file_path=trace_file_name,
            )
            print(raw_output)

            print()

    @register_command(aliases={"action"})
    def do(self):
        """Run gitlabcicli do."""

        for job_id in self.args["job_ids"]:
            response = self.api_client.run_action_on_job(
                action=self.args["job_action"],
                job_id=job_id,
                project_id=self.project_id,
            )
            debug(response, 5)

            if not response:
                error(
                    f"Could not {self.args['job_action']} job #{job_id} for project '{self.project}'."
                )
            else:
                past = {"cancel": "canceled", "retry": "retried", "erase": "erased"}
                cprint(
                    f"Successfully {self.args['job_action']} job #{job_id} for project '{self.project}'",
                    color="green",
                    attrs=["bold"],
                )

                if self.args["job_action"] == "retry":
                    cprint(
                        f"New job id is #{response['id']}",
                        color="green",
                        attrs=["bold"],
                    )

    @register_command(aliases={"validate"})
    def lint(self):
        """Run gitlabcicli lint."""
        gitlabciyml_text = self.args["file"].read()
        debug(f"gitlabci.yml content:\n{gitlabciyml_text}", 5)
        api = self.api_client.validate_ciyml(gitlabciyml_text=gitlabciyml_text)

        if api["status"] == "valid":
            cprint(
                ".gitlab-ci.yml is valid",
                color="green",
                attrs=["bold"],
            )
        else:
            cprint(
                ".gitlab-ci.yml is invalid",
                color="red",
                attrs=["bold"],
            )
            print("List of errors:")

            for error_description in api["errors"]:
                print(f" - {error_description}")

    @register_command(aliases={"web"})
    def open(self):
        """Open the current project in browser."""
        url = self.api_client.get_project_url(self.project_id)
        os.system(f"xdg-open {url}")

    @register_command(aliases={"exec"})
    def run_local(self):
        """Run pipeline on local machine."""
        raise NotImplementedError(
            "run_local is not yet implemented. Contribution is welcome."
        )

    @register_command(aliases={"start"})
    def init(self):
        """Create a .gitlab-ci.yml."""
        # TODO ensure this is in git root
        file_path = Path(".gitlab-ci.yml")

        if file_path.is_file():
            error(f"{file_path} already exists")

        with open(file_path, "w") as file:
            print("---", file=file)
            print("# TODO write here", file=file)
            print("", file=file)
            print("...", file=file)

        print(f"{file_path} created.")


def parse_args():
    """Return the parsed arguments as object (see argparse doc)."""
    # TODO use info from COMMANDS
    parser = argparse.ArgumentParser(description=info.__doc__)
    parser.add_argument(
        "--version", action="version", version="%(prog)s {info.__version__}"
    )
    parser.add_argument(
        "-v",
        dest="verbosity",
        action="count",
        default=0,
        help="Be more verbose (up to -vvvvv)",
    )
    parser.add_argument(
        "-t",
        "--ask-for-token",
        action="store_true",
        help="Ask for the GitLab access token using stdin to query the API.",
    )
    parser.add_argument(
        "-s",
        "--server",
        metavar="URL",
        dest="server_url",
        help="The gitlab server url"
        + "(e.g.: https://gitlab.com/, default: parsed from remote)",
    )
    parser.add_argument(
        "-p",
        "--project",
        help="The project name or id (e.g. foo/bar, default: current project)",
    )

    subparsers = parser.add_subparsers(
        title="actions",
        dest="action",
        # required=False, TODO
    )

    # show
    parser_show = subparsers.add_parser(
        "show",
        aliases=COMMANDS["show"].aliases,
        help="Show the current job status",
    )
    parser_show.add_argument(
        "-c",
        "--commit",
        type=get_long_commit_sha,
        metavar="SHA",
        dest="commit_hash",
        help="The commit id to check (default: the current id)",
    ).completer = sha_completer
    parser_show.add_argument(
        "-j",
        "--job",
        metavar="ID",
        dest="job_ids",
        type=int,
        action="append",
        default=[],
        help="The job id to inspect",
    )

    # raw
    parser_raw = subparsers.add_parser(
        "raw",
        aliases=COMMANDS["raw"].aliases,
        help="Get or watch the output of a job",
    )
    parser_raw.add_argument(
        "-f",
        "--follow",
        action="store_true",
        default=False,
        help="Follow running jobs (default: false)",
    )
    parser_raw.add_argument(
        "-c",
        "--commit",
        type=get_long_commit_sha,
        metavar="SHA",
        dest="commit_hash",
        help="The commit id to inspect (default: the current id)",
    ).completer = sha_completer
    parser_raw.add_argument(
        "-j",
        "--job",
        metavar="ID",
        dest="job_ids",
        type=int,
        action="append",
        default=[],
        help="The job id to inspect",
    )

    # do
    parser_do = subparsers.add_parser(
        "do",
        aliases=COMMANDS["do"].aliases,
        help="Run actions on jobs [cancel, retry, erase]",
    )
    parser_do.add_argument(
        "job_action",
        metavar="action",
        choices=("cancel", "retry", "erase"),
        help="What to do with the job [cancel, retry, erase]",
    )
    parser_do.add_argument(
        "-j",
        "--job",
        metavar="ID",
        dest="job_ids",
        type=int,
        action="append",
        required=True,
        help="The job id to inspect",
    )

    # lint
    parser_lint = subparsers.add_parser(
        "lint",
        aliases=COMMANDS["lint"].aliases,
        help="Validate the gitlab-ci.yml",
    )
    parser_lint.add_argument(
        "file",
        type=argparse.FileType("r"),
        default=".gitlab-ci.yml",
        nargs="?",
        help="The gitlab-ci.yml",
    ).completer = gitlabciyml_completer

    # open
    parser_open = subparsers.add_parser(
        "open",
        aliases=COMMANDS["open"].aliases,
        help="Open the current project in your browser.",
    )

    # run local
    parser_run_local = subparsers.add_parser(
        "run-local",
        aliases=COMMANDS["run-local"].aliases,
        help="Run a stage on the local machine.",
    )

    # init
    parser_init = subparsers.add_parser(
        "init",
        aliases=COMMANDS["init"].aliases,
        help="Create a .gitlab-ci.yml",
    )

    if argcomplete:
        argcomplete.autocomplete(parser)

    args = parser.parse_args()

    if args.verbosity > 5:
        args.verbosity = 5
    set_verbosity(args.verbosity)

    if not args.action:
        args.action = "show"

    if args.action not in COMMANDS.keys():
        for command_name, command in COMMANDS.items():
            if args.action in command.aliases:
                args.action = command_name

                break

    return args


def main():
    """The main function"""
    args = parse_args()

    action = COMMANDS[args.action]

    cli = GitLabCiCli(**args.__dict__)
    getattr(cli, action.name)()
    cli.stop()


if __name__ == "__main__":
    main()
