#! /usr/local/bin/python3

"""Docker Engine API available as a script.
Used for isolating the levo user from direct access to the docker socket.
"""
import datetime
import json
import sys
from typing import Any

import docker

_CLI_REPO_NAME = "levoai/levo"
_DOCKER_SOCK = "unix://var/run/docker.sock"


def _list_local_images() -> None:
    local_images: list[dict[Any, Any]] = []
    try:
        client = docker.DockerClient(base_url=_DOCKER_SOCK)
        images: list[docker.Image] = client.images.list(name=_CLI_REPO_NAME)

        for image in images:
            created_epoch = int(image.history()[0]["Created"])
            created_on: str = "*unknown*"
            try:
                created_dt: datetime.datetime = datetime.datetime.fromtimestamp(
                    created_epoch
                )
                created_on = str(created_dt)
            except:
                pass

            for i in range(len(image.tags)):
                local_images.append(
                    {
                        "tag": image.tags[i],
                        "created_on": created_on,
                        "id": image.id,
                        "short_id": image.short_id,
                    }
                )
    except:
        print('{ "status" : "error" }')
        return

    resp: dict[str, Any] = {"status": "success"}
    resp["images"] = local_images
    print(json.dumps(resp, indent=2))
    return


def _remove_image(image_tag: str) -> None:
    try:
        client = docker.DockerClient(base_url=_DOCKER_SOCK)
        client.images.remove(image=_CLI_REPO_NAME + ":" + image_tag)
    except:
        print('{ "status" : "error" }')
        return

    print('{ "status" : "success" }')
    return


def _pull_image(image_tag: str) -> None:
    try:
        client = docker.DockerClient(base_url=_DOCKER_SOCK)
        pulled_img: docker.Image = client.images.pull(
            repository=_CLI_REPO_NAME, tag=image_tag
        )
    except:
        print('{ "status" : "error" }')
        return

    resp: dict[str, Any] = {"status": "success"}
    resp["image"] = {
        "id": pulled_img.id,
        "short_id": pulled_img.short_id,
        "tags": pulled_img.tags,
    }
    print(json.dumps(resp, indent=2))
    return


def _tag_image(image_tag: str, new_image_tag: str) -> None:
    try:
        client = docker.DockerClient(base_url=_DOCKER_SOCK)
        img_to_tag: docker.Image = client.images.get(
            name=_CLI_REPO_NAME + ":" + image_tag
        )

        if not img_to_tag.tag(repository=_CLI_REPO_NAME, tag=new_image_tag):
            raise docker.errors.APIError
    except:
        print('{ "status" : "error" }')
        return

    print('{ "status" : "success" }')
    return


def _main() -> None:
    args_len: int = len(sys.argv) - 1
    if len(sys.argv) < 1:
        return

    if sys.argv[1] == "list_images":
        _list_local_images()
    elif sys.argv[1] == "remove_image" and args_len == 2:
        _remove_image(image_tag=sys.argv[2])
    elif sys.argv[1] == "pull_image" and args_len == 2:
        _pull_image(image_tag=sys.argv[2])
    elif sys.argv[1] == "tag_image" and args_len == 3:
        _tag_image(image_tag=sys.argv[2], new_image_tag=sys.argv[3])

    return


if __name__ == "__main__":
    _main()
