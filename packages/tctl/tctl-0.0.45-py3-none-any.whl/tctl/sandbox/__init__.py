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
    "bar": "     Send a bar Tradehook to the specified url: --url|-u {URL OF STRATEGY}",
    "monitor": " Send a monitor Tradehook to the specified url: --url|-u {URL OF STRATEGY}",
    "price": "   Send a price monitor Tradehook to the specified url: --url|-u {URL OF STRATEGY}",
    "position": " Send a position monitor Tradehook to the specified url: --url|-u {URL OF STRATEGY}",
    "order": "   Send an order Tradehook to the specified url: --url|-u {URL OF STRATEGY}",
    "error": "   Send an error Tradehook to the specified url: --url|-u {URL OF STRATEGY}",
}

rules = utils.args_actions()
commands = rules.add_symlinks(commands)

rules.add_flags(["price", "position", "monitor"], {
    "expired": ["--expired"]
})

rules.add_required(["order", "monitor"], {
    "kind": ["-k", "--kind"],
    "url": ["-u", "--url"]
})

rules.add_required(["price", "position", "bar", "error"], {
    "url": ["-u", "--url"]
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
def sandbox(options):
    """Send Tradehooks to a URL for development testing"""
    command, options = options

    # -- fix url ---
    argv = " ".join(sys.argv)
    options['url'][0] = options.first('url') + argv.split(options.first('url'))[1].split(' ')[0]
    # -- /fix url ---

    if command == "bar":
        crud.sandbox_bar(options)

    if command == "order":
        crud.sandbox_order(options)

    if command == "monitor":
        if options.first('kind') == 'position':
            crud.sandbox_position(options)
        else:
            crud.sandbox_price(options)

    if command == "price":
        crud.sandbox_price(options)

    if command == "position":
        crud.sandbox_position(options)

    if command == "error":
        crud.sandbox_error(options)
