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
    "ls": "  Retrieve " + command + " history: [--connection|-c{CONNECTION_ID}] [--strategy|-s {STRATEGY_ID}] "
                                    "[--start {DATETIME}] [--end {DATETIME}]",
    "orders": " Retrieve position orders: (required) [--position|-p  {POSITION_ID}]",
}

rules = utils.args_actions()
commands = rules.add_symlinks(commands)
rules.add_optional("list", {
    "connection": ["-c", "--connection"],
    "strategy": ["-s", "--strategy"],
    "start": ["--start"],
    "end": ["--end"],
})

rules.add_required("orders", {
    "position": ["-p", "--position"]
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
def positions(options):
    """Retreive position history with filtering options"""
    command, options = options

    if command in ["ls", "list"]:
        crud.positions_list(options)

    if command == "orders":
        crud.position_orders_list(options)
