#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import click
import sys
from .. import utils
from . import crud

try:
    command = sys.argv[1]
except:
    command = ""

commands = {
    "list": "Retrieve volume list [--show-ids]",
    "new": "Create new volume [-r|--region {REGION}] [-n|--name {NAME}] [-s|--size {SIZE}]",
    "retrieve": "Retrieve volume [--id {VOLUME_UUID}]",
    "modify": "Modify volume [--id {VOLUME_UUID}] [-n|--name {NEW_NAME}]",
    "detach": "Detach volume from instance [--id {VOLUME_UUID}]",
    "attach": "Attach volume to instance [--vid {VOLUME_UUID}] [--iid {INSTANCE_UUID}]",
    "delete": "Delete volume [--id {VOLUME_UUID}]"
}


rules = utils.args_actions()
commands = rules.add_symlinks(commands)

rules.add_optional(["list", "ls"], {
    "page_limit": ["-pl", "--page-limit"],
    "page": ["-p", "--page"],
    "order_by": ["--order-by"]
})

rules.add_optional(["new"], {
    "name": ["-n", "--name"],
    "size": ["-s", "--size"],
    "region": ["-r", "--region"]
})

rules.add_required(["retrieve", "delete", "detach"], {
    "id": ["--id"]
})

rules.add_required(["modify"], {
    "id": ["--id"],
    "name": ["-n", "--name"]
})


rules.add_required(["attach"], {
    "vid": ["--vid"],
    "iid": ["--iid"]
})

rules.add_flags(["ls", "list"], {
    "ids": ["--show-ids"]
})


def options_validator(ctx, param, args):
    return utils.options_validator(args, commands, rules)


@click.group()
def cli():
    pass


# router function
@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument('options', nargs=-1, type=click.UNPROCESSED,
                callback=options_validator)
def volumes(options):
    """List, retrieve, modify, delete, create research volumes"""
    command, options = options

    if command in ["ls", "list"]:
        crud.volumes_list(options)

    if command == "new":
        crud.create_volume(options)

    if command == "retrieve":
        crud.retrieve_volume(options)

    if command == "modify":
        crud.modify_volume(options)

    if command == "detach":
        crud.detach_volume(options)

    if command == "attach":
        crud.attach_volume(options)

    if command == "delete":
        crud.delete_volume(options)



