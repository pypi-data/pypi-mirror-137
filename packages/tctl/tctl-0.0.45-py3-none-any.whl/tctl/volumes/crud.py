#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import sys
import click
from .. import utils
from .. import inputs
from .. import remote
import pandas as pd


def volumes_list(options):

    endpoint = "/volumes"
    data, errors = remote.api.get(endpoint)

    if options.get("raw"):
        if not data:
            click.echo("\n[]")
        else:
            click.echo(utils.to_json(data, errors))

        return

    if not data:
        click.echo("\nNo volumes found.")
        return

    cols = ['name', 'region', 'status', 'size', 'attached_instance']

    if options.first('ids', False):
        cols = ['id'] + cols
    table_data = pd.DataFrame(data)
    table_data = table_data[[col for col in cols if col in table_data.columns]]

    if len(table_data) > 20:
        click.echo_via_pager(utils.to_table(table_data))
    else:
        click.echo(utils.to_table(table_data))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def create_volume(options):

    endpoint = "/volumes"

    click.echo("")
    name = options.first('name')
    size = options.first('size')
    region = options.first('region')

    while name == "" or name is None:
        name = inputs.text("Instance name")

    while size == "" or size is None:
        size = inputs.integer("Size (in GB)")

    if not region:
        region = inputs.option_selector(
            "Region", [
                'us-east-1', 'us-east-2', 'us-west-2',
                'eu-central-1', 'eu-west-1', 'ap-southeast-1'])

    payload = {
        'name': name,
        'size': size,
        'region': region
    }

    data, errors = remote.api.post(endpoint, json=payload)

    if options.get("raw"):
        if not data:
            click.echo("\n[]")
        else:
            click.echo(utils.to_json(data, errors))

        return

    cols = ['id', 'name', 'region', 'status', 'size', 'attached_instance']

    table_data = pd.DataFrame(data, index=[0])
    table_data = table_data[[col for col in cols if col in table_data.columns]]

    if len(table_data) > 20:
        click.echo_via_pager(utils.to_table(table_data))
    else:
        click.echo(utils.to_table(table_data))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def retrieve_volume(options):

    endpoint = f"/volume/{options.first('id')}"

    data, errors = remote.api.get(endpoint)

    if options.get("raw"):
        if not data:
            click.echo("\n[]")
        else:
            click.echo(utils.to_json(data, errors))

        return

    cols = ['id', 'name', 'region', 'status', 'size', 'attached_instance']

    table_data = pd.DataFrame(data, index=[0])
    table_data = table_data[[col for col in cols if col in table_data.columns]]

    if len(table_data) > 20:
        click.echo_via_pager(utils.to_table(table_data))
    else:
        click.echo(utils.to_table(table_data))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def modify_volume(options):

    endpoint = f"/volume/{options.first('id')}"

    payload = {
        'name': options.first('name')
    }

    data, errors = remote.api.patch(endpoint, json=payload)

    if options.get("raw"):
        if not data:
            click.echo("\n[]")
        else:
            click.echo(utils.to_json(data, errors))

        return

    cols = ['id', 'name', 'region', 'status', 'size', 'attached_instance']

    table_data = pd.DataFrame(data, index=[0])
    table_data = table_data[[col for col in cols if col in table_data.columns]]

    if len(table_data) > 20:
        click.echo_via_pager(utils.to_table(table_data))
    else:
        click.echo(utils.to_table(table_data))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def detach_volume(options):
    endpoint = f"/volume/{options.first('id')}/detach"

    data, errors = remote.api.patch(endpoint)

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))

    click.echo(f"Volume {options.first('id')} has been successfully defatched")


def attach_volume(options):

    endpoint = f"/volumes/{options.first('vid')}/attach/{options.first('iid')}"

    data, errors = remote.api.patch(endpoint)

    if options.get("raw"):
        if not data:
            click.echo("\n[]")
        else:
            click.echo(utils.to_json(data, errors))

        return

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))

    click.echo(f"Volume {options.first('vid')} has been successfully attached to instance {options.first('iid')}")


def delete_volume(options):

    endpoint = f"/volume/{options.first('id')}"

    data, errors = remote.api.delete(endpoint)

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))

    utils.success_response(
        f"Volume {options.first('id')} has been deleted successfully.")
