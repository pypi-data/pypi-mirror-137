"""Docker Image Management Sub commands"""

import json
import logging
import os
import re
import subprocess
from typing import Any, List

import click
import requests
from click_loglevel import LogLevel

from levocli.commands.constants import CONTEXT_SETTINGS

from ..logger import get_logger, set_log_level

log = get_logger(__name__)

_CLI_REPO_NAME = "levoai/levo"
_HUB_AUTH_URL = "https://auth.docker.io/token?service=registry.docker.io&scope=repository:levoai/levo:pull"
_HUB_TAGS_URL = "https://index.docker.io/v2/levoai/levo/tags/list"
_HUB_IMAGE_MANIFEST_PREFIX = "https://index.docker.io/v2/levoai/levo/manifests/"


"""Helper functions"""


def _get_docker_hub_token() -> str:
    """Get the access token from Docker Hub.
    Returns an access token or null string.
    """
    access_token = ""
    try:
        resp = requests.get(_HUB_AUTH_URL)
        resp.raise_for_status()
        respJSON = resp.json()
        access_token = respJSON["access_token"]
    except Exception as e:
        log.debug("Error getting Docker Hub access token.", exception=e)
        pass

    return access_token


def _get_docker_hub_image_tags() -> tuple[bool, List[str]]:
    """Get the tags for the CLI image. Returns True on success."""
    token: str = _get_docker_hub_token()
    if not token:
        return False, []

    try:
        headers = {"Authorization": "Bearer " + token}
        response = requests.get(_HUB_TAGS_URL, headers=headers)
        response.raise_for_status()
        responseJSON = response.json()
        tags = responseJSON["tags"]
    except Exception as e:
        log.debug("Error getting image tags from Docker Hub.", exception=e)
        return False, []

    return True, tags


def _error_exit() -> None:
    click.echo()
    click.secho("Error listing CLI images on Docker Hub.", fg="red")
    raise click.exceptions.Exit(1)
    # End of execution


def _get_docker_hub_image_summary(image_tag: str) -> tuple[bool, dict[str, str]]:
    """Get the summary info for specified CLI image tag. Returns True on success."""
    token: str = _get_docker_hub_token()
    if not token:
        return False, {}

    try:
        headers = {"Authorization": "Bearer " + token}
        url = _HUB_IMAGE_MANIFEST_PREFIX + image_tag

        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        respJSON = response.json()

        summary: dict[str, str] = {}
        summary["name"] = respJSON["name"]
        summary["tag"] = respJSON["tag"]

        compat_str: str = respJSON["history"][0]["v1Compatibility"]
        compat_obj = json.loads(compat_str)

        summary["id"] = compat_obj["id"]
        summary["created"] = compat_obj["created"]
    except Exception as e:
        log.debug("Error getting image summary from Docker Hub.", exception=e)
        return False, {}

    return True, summary


def _list_hub_images() -> None:
    """List all CLI images on Docker Hub."""
    status, tagged_images = _get_docker_hub_image_tags()
    if not status:
        _error_exit()

    click.secho("{:<35} {:<15}".format("Image Name/Tag", "Creation Time"), fg="green")
    click.echo("{:<35} {:<15}".format("--------------", "-------------"))

    image: str
    for image in tagged_images:
        status, image_info = _get_docker_hub_image_summary(image_tag=image)
        if status:
            click.echo(
                "{:<35} {:<15}".format(
                    _CLI_REPO_NAME + ":" + image, image_info["created"]
                )
            )

    return


def _invoke_docker_api(cmd_args: List[str]) -> dict[str, Any]:
    """The docker API is invoked via a script in a sub process.
    The script has sudo privileges for the levo user in the container.
    This is required as we don't want to run the container as root.
    """
    try:
        abspath = os.path.abspath(__file__)
        parent_dir = abspath.removesuffix("/commands/image.py")
        api_path: str = parent_dir + "/docker_api/docker_api.py"

        popen_args = ["/usr/bin/sudo", api_path]
        popen_args.extend(cmd_args)
        stdout = subprocess.run(
            popen_args, check=True, capture_output=True, text=True
        ).stdout

        jsonResp = json.loads(stdout)
    except Exception as e:
        log.debug("Error invoking Docker API: ", exception=e)
        return {"status": "error"}

    return jsonResp


def _list_local_images() -> None:
    images_info: dict[str, Any] = _invoke_docker_api(cmd_args=["list_images"])
    if images_info["status"] == "error":
        log.debug("Error listing local CLI images.")
        click.echo()
        click.secho("Error listing local CLI images.", fg="red")
        raise click.exceptions.Exit(1)

    click.secho(
        "{:<30} {:<20} {:<15}".format("Image Name/Tag", "Short ID", "Creation Time"),
        fg="green",
    )
    click.echo(
        "{:<30} {:<20} {:<15}".format("--------------", "--------", "-------------")
    )

    for image in images_info["images"]:
        click.echo(
            "{:<30} {:<20} {:<15}".format(
                image["tag"], image["short_id"], image["created_on"]
            )
        )

    return


def _get_pinned_image_tag() -> str:
    """Get pinned image tag if exists or empty string. Throws exception on error."""
    images_info: dict[str, Any] = _invoke_docker_api(cmd_args=["list_images"])
    if images_info["status"] == "error":
        log.debug("Error listing local CLI images.")
        raise RuntimeError

    for image in images_info["images"]:
        tag: str = image["tag"]
        if tag.endswith("-pinned"):
            return tag.lstrip(_CLI_REPO_NAME + ":")

    return ""


def _unpin_image(pinned_image: str) -> bool:
    if not pinned_image or not pinned_image.endswith("-pinned"):
        return False

    result: dict[str, Any] = _invoke_docker_api(cmd_args=["remove_image", pinned_image])
    if result["status"] == "error":
        return False

    return True


def _upgrade_image() -> bool:
    result: dict[str, Any] = _invoke_docker_api(cmd_args=["pull_image", "stable"])
    if result["status"] == "error":
        return False

    return True


def _pin_image(tag_to_pin: str) -> bool:
    new_tag = tag_to_pin + "-pinned"
    result: dict[str, Any] = _invoke_docker_api(
        cmd_args=["tag_image", tag_to_pin, new_tag]
    )
    if result["status"] == "error":
        return False

    return True


""" End of Helper Functions Section"""


"""Image manament sub commands"""


@click.group(context_settings=CONTEXT_SETTINGS)
def image():
    """CLI Docker image management sub commands."""
    return


@image.command(short_help="List CLI images in the specified repository.")
@click.option(
    "--repo",
    "-r",
    type=click.Choice(["local", "hub"], case_sensitive=False),
    default="local",
    help="The repository to list. 'local' is your image cache, and 'hub' is Docker Hub.",
    show_default=True,
    required=True,
)
@click.option(
    "-v",
    "--verbosity",
    type=LogLevel(),
    default=logging.WARN,
)
def list(
    repo: str,
    verbosity: LogLevel,
):
    """List all CLI images in the specified repository."""
    set_log_level(int(verbosity))

    if repo and repo == "hub":
        _list_hub_images()
    else:
        _list_local_images()


@image.command(
    short_help="Upgrade the CLI Docker image to the latest `stable` tagged version."
)
@click.option(
    "--force",
    "-f",
    help="Force upgrade even if you have pinned to a specific version tag.",
    is_flag=True,
    default=False,
    show_default=True,
)
@click.option(
    "-v",
    "--verbosity",
    type=LogLevel(),
    default=logging.WARN,
)
def upgrade(
    force: bool,
    verbosity: LogLevel,
):
    """Upgrade the CLI Docker image to the latest `stable` tagged version."""
    set_log_level(int(verbosity))

    try:
        pinned_image: str = _get_pinned_image_tag()
        if pinned_image and not force:
            click.echo()
            click.secho(
                "You have a pinned image: {}. Use --force to force an upgrade.".format(
                    "`" + _CLI_REPO_NAME + ":" + pinned_image + "`"
                ),
                fg="yellow",
            )
            raise click.exceptions.Exit(1)

        # Unpin image before upgrade
        if pinned_image and (not _unpin_image(pinned_image)):
            click.echo()
            click.secho("Error: cannot continue, failed to unpin image.", fg="red")
            raise click.exceptions.Exit(1)

        click.echo("Proceeding to upgrade image. This may take a few seconds ...")
        if not _upgrade_image():
            click.echo()
            click.secho("Error: failed to upgrade image.", fg="red")
            raise click.exceptions.Exit(1)
    except:
        click.echo()
        click.secho("Error: failed to upgrade image.", fg="red")
        raise click.exceptions.Exit(1)

    click.echo()
    click.secho(
        "Your image has been upgraded to the latest `stable` tagged version.",
        fg="green",
    )
    return


@image.command(
    short_help="Pin the CLI Docker image to a specific (numerically tagged) version."
)
@click.option(
    "--version",
    help="The version number that you want to pin. E.g. `1.0.0`.",
    type=str,
    required=True,
)
@click.option(
    "-v",
    "--verbosity",
    type=LogLevel(),
    default=logging.WARN,
)
def pin(
    version: str,
    verbosity: LogLevel,
):
    """Pin the CLI Docker image to a specific (numerically tagged) version."""
    set_log_level(int(verbosity))

    pinned_image: str = _get_pinned_image_tag()
    if pinned_image:
        click.echo()
        click.secho(
            "You have a pinned image: {}. You must unpin the image first.".format(
                "`" + _CLI_REPO_NAME + ":" + pinned_image + "`"
            ),
            fg="red",
        )
        raise click.exceptions.Exit(1)

    # Only numerical versions are allowed to be pinned
    matched = re.match("[0-9]\.[0-9]\.[0-9]", version)
    if not bool(matched):
        click.echo()
        click.secho("Only numeric versions are allowed to be pinned.", fg="red")
        raise click.exceptions.Exit(1)

    if not _pin_image(tag_to_pin=version):
        click.echo()
        click.secho("Error pinning the specified image.", fg="red")
        raise click.exceptions.Exit(1)

    click.echo()
    click.secho(
        "Successfully pinned the specified image. Levo CLI will use this pinned version for all future invocations.",
        fg="green",
    )
    return


@image.command(
    short_help="Unpin the CLI from using a previously pinned Docker image version."
)
@click.option(
    "-v",
    "--verbosity",
    type=LogLevel(),
    default=logging.WARN,
)
def unpin(
    verbosity: LogLevel,
):
    """Unpin the CLI from using a previously pinned Docker image version."""
    set_log_level(int(verbosity))

    pinned_image: str = _get_pinned_image_tag()
    if not pinned_image:
        click.echo()
        click.secho("You do not have a pinned image to unpin.", fg="yellow")
        raise click.exceptions.Exit(1)

    if not _unpin_image(pinned_image=pinned_image):
        click.echo()
        click.secho("Error unpinning the previously pinned version.", fg="red")
        raise click.exceptions.Exit(1)

    click.echo()
    click.secho(
        "Success. Levo CLI will use the 'stable' image version for all future invocations.",
        fg="green",
    )
    return
