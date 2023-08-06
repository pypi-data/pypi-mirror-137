#!/usr/bin/env python

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
    "orders": " Retrieve trade orders: (required) [--trade|-t  {TRADE_ID}]",
    "positions": " Retrieve trade positions: (required) [--trade|-t  {TRADE_ID}]",
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
    "trade": ["-t", "--trade"]
})

rules.add_required("positions", {
    "trade": ["-t", "--trade"]
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
def trades(options):
    """Retreive trade history with filtering options"""
    command, options = options

    if command in ["ls", "list"]:
        crud.trades_list(options)

    if command == "orders":
        crud.trade_orders_list(options)

    if command == "positions":
        crud.trade_positions_list(options)
