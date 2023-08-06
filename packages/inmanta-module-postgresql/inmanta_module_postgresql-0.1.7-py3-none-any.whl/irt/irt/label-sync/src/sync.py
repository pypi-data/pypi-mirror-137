"""
    Copyright 2020 Inmanta

    Contact: code@inmanta.com
"""
import logging
import os
import sys
from typing import List

import click
import github_label_sync
import requests

LOGGER = logging.getLogger(__name__)

GITHUB_API_URL = "https://api.github.com"
DEFAULT_LABELS_PATH = os.path.realpath(
    os.path.join(os.path.dirname(__file__), "..", "labels.json")
)


def get_repositories(github_access_token: str):
    next = f"{GITHUB_API_URL}/orgs/inmanta/repos"
    repositories = []

    while next is not None:
        response = requests.get(
            next,
            headers={"Authorization": f"token {github_access_token}"},
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"And error occurred while resolving all inmanta repositories: {response.status_code}"
            )

        repositories.extend(
            [
                repository["full_name"]
                for repository in response.json()
                if not repository["archived"]
            ]
        )

        if "next" in response.links.keys():
            next = response.links["next"]["url"]
        else:
            next = None

    return_and_tab = "\n\t"
    LOGGER.debug(
        f"Retrieved {len(repositories)} repository from inmanta project: {return_and_tab}{return_and_tab.join(repositories)}"
    )
    return repositories


@click.command()
@click.option(
    "-a",
    "--all",
    help="Apply the operations on all repositories of project inmanta",
    is_flag=True,
)
@click.option(
    "--delete",
    help="Delete labels present on repository but not in input file",
    is_flag=True,
)
@click.option(
    "--dry-run",
    help="Perform a dry-run only, check if all repositories are in sync",
    is_flag=True,
)
@click.option(
    "--github-access-token",
    help="Overwrite GITHUB_ACCESS_TOKEN environment variable, which allows to use the Github API",
    envvar="GITHUB_ACCESS_TOKEN",
    is_flag=False,
    required=True,
)
@click.option(
    "-l",
    "--labels",
    help="Path to a file containing all labels to apply",
    default=DEFAULT_LABELS_PATH,
    is_flag=False,
    show_default=True,
)
@click.option(
    "--log-level",
    help="Specifiy the logging level",
    default="WARNING",
    show_default=True,
)
@click.option(
    "-y",
    "--yes",
    help="Don't prompt and ask for confirmation before applying modifications",
    is_flag=True,
)
@click.argument("repositories", nargs=-1)
def main(
    all: bool,
    delete: bool,
    dry_run: bool,
    github_access_token: str,
    labels: str,
    log_level: str,
    yes: bool,
    repositories: List[str],
):
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: %s" % log_level)
    logging.basicConfig(level=numeric_level)

    if not os.path.isfile(labels):
        LOGGER.error(f"Not label file found at {labels}")
        sys.exit(1)

    if all:
        repositories = get_repositories(github_access_token)

    if len(repositories) == 0:
        LOGGER.warning("No repositories were provided, skipping checks")
        sys.exit(0)

    has_changes = False
    for change in github_label_sync.dry_run(
        labels, repositories, github_access_token, delete_additionals=delete
    ):
        has_changes = True
        print(change)

    if not has_changes:
        LOGGER.info("No change to apply")
        sys.exit(0)

    if dry_run:
        LOGGER.error("Dry-run detected changes to apply")
        sys.exit(1)

    apply_changes = yes
    if not yes:
        apply_changes = "yes" == input(
            "Please confirm that you wish to apply all those changes (yes): "
        )

    if not apply_changes:
        LOGGER.warning("Skipping changes as user wished it")
    else:
        for operation in github_label_sync.sync(
            labels, repositories, github_access_token, delete_additionals=delete
        ):
            print(f"Applied: {operation}")

    sys.exit(0)


if __name__ == "__main__":
    main()
