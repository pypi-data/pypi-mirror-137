#!/usr/bin/env python

import click
from .. import utils
from . import crud


commands = {
    "list": "Retreive connections list",
    "info": "Show connection information: --connection|-c {CONNECTION_ID}",
    "new": "Create new connection",
    "update": "Update existing connection: --connection|-c {CONNECTION_ID}",
    "delete": "Delete connection: --connection|-c {CONNECTION_ID}",
}

rules = utils.args_actions()
commands = rules.add_symlinks(commands)

for command in ["info", "update", "patch", "delete"]:
    rules.add_required(command, {"connection": ["-c", "--connection"]})


def options_validator(ctx, param, args):
    return utils.options_validator(args, commands, rules)


@click.group()
def cli():
    pass


# router function
@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument('options', nargs=-1, type=click.UNPROCESSED,
                callback=options_validator)
def connections(options):
    """List, create, update, or delete connections"""
    command, options = options
    # print(command, options)

    if command in ["ls", "list"]:
        crud.connections_list(options)

    elif command == "info":
        crud.connection_info(options)

    elif command == "new":
        crud.connection_create(options)

    elif command in ["update", "patch"]:
        crud.connection_update(options)

    elif command in ["rm", "delete"]:
        crud.connection_delete(options)
