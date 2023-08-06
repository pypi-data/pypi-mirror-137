#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import click
import sys
from .. import utils
from . import crud
import pandas as pd


pd.options.display.float_format = '{:,}'.format

try:
    command = sys.argv[1]
except:
    command = ""

commands = {
    "list": "Retrieve instance list [--show-ids]",
    "new": "Create new instance [--region|-r {REGION}] [--name|-n {INSTANCE_NAME}] [--type|-t {TYPE}]",
    "retrieve": "Retrieve instance [--id {INSTANCE_UUID}]",
    "jupyter": "Open instance via Jupyter [--id {INSTANCE_UUID}]",
    "vsc": "Open instance via VS Code [--id {INSTANCE_UUID}]",
    "modify": "Modify instance [--id {INSTANCE_UUID}] [--name|-n {NEW_NAME}]",
    "detach": "Detach volume from instance [--id {INSTANCE_UUID}]",
    "attach": "Attach volume to instance [--vid {VOLUME_UUID}] [--iid {INSTANCE_UUID}]",
    "delete": "Delete instance [--id {INSTANCE_UUID}]"
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
    "region": ["-r", "--region"],
    "type": ["-t", "--type"]
})


rules.add_required(["retrieve", "delete", "detach", "jupyter", "vsc"], {
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
def instances(options):
    """List, retrieve, modify, delete, create research instances"""
    command, options = options

    if command in ["ls", "list"]:
        crud.instances_list(options)

    if command == "new":
        crud.create_instance(options)

    if command == "retrieve":
        crud.retrieve_instance(options)

    if command == "modify":
        crud.modify_instance(options)

    if command == "detach":
        crud.detach_volume(options)

    if command == "attach":
        crud.attach_volume(options)

    if command == "delete":
        crud.delete_instance(options)

    if command == "jupyter":
        crud.jupyter(options)

    if command == "vsc":
        crud.vscode(options)
