#!/usr/bin/env python

import click

# internals
from . import credentials
from . import terminal


@click.group()
def cli():
    pass

@cli.command()
def logo():
    """Displays Tradologics logo as ASCII art :)"""
    click.echo(terminal.logo)


@cli.command()
@click.option('--delete', is_flag=True, help="Deletes token from disk.")
@click.option('--key', help="API Key")
@click.option('--secret', help="API Secret")
@click.option('--dnt', default=False, is_flag=True, help="Track Install?", hidden=True)
def config(delete, key, secret, dnt):
    """Initialize, authorize, and configure the tctl tool

    Retreives and stores your token in as an encrypted file on disk.
    """
    if delete:
        credentials.delete()

    return credentials.config(
        source="config", api_key=key, api_secret=secret, dnt=dnt)
