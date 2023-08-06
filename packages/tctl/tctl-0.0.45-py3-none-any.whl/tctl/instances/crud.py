#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import sys
import click
import pandas as pd

from .. import utils
from .. import remote
from .. import inputs


def instances_list(options):

    endpoint = "/instances"
    data, errors = remote.api.get(endpoint)

    if options.get("raw"):
        if not data:
            click.echo("\n[]")
        else:
            click.echo(utils.to_json(data, errors))

        return

    if not data:
        click.echo("\nNo instances found.")
        return

    cols = ['name', 'hostname', 'region', 'type', 'cpu', 'storage', 'memory', 'status', 'host', 'attached_volume']

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


def create_instance(options):
    endpoint = "/instances"

    click.echo("")
    name = options.first('name')
    itype = options.first('type')
    region = options.first('region')

    while name == "" or name is None:
        name = inputs.text("Instance name")

    if not itype:
        types = {
            'Balanced': 'b.',
            'CPU-Optimized': 'c.',
            'Memory-Optimized': 'm.'
        }
        ctype = inputs.option_selector(
            "Please select type", list(types.keys()))
        stype = inputs.option_selector(
            "Please select size", ['Small', 'Medium', 'Large', 'XLarge'])
        itype = types[ctype] + stype.lower()

    if not region:
        region = inputs.option_selector(
            "Region", [
                'us-east-1', 'us-east-2', 'us-west-2',
                'eu-central-1', 'eu-west-1', 'ap-southeast-1'])

    payload = {
        'name': name,
        'type': itype,
        'region': region
    }

    data, errors = remote.api.post(endpoint, json=payload)

    if options.get("raw"):
        if not data:
            click.echo("\n[]")
        else:
            click.echo(utils.to_json(data, errors))

        return

    cols = ['id', 'name', 'hostname', 'region', 'type', 'cpu', 'storage', 'memory', 'status', 'host', 'attached_volume']

    table_data = pd.DataFrame(data, index=[0])
    table_data = table_data[[col for col in cols if col in table_data.columns]]

    if len(table_data) > 20:
        click.echo_via_pager(utils.to_table(table_data))
    else:
        click.echo(utils.to_table(table_data))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def retrieve_instance(options):

    endpoint = f"/instance/{options.first('id')}"

    data, errors = remote.api.get(endpoint)

    if options.get("raw"):
        if not data:
            click.echo("\n[]")
        else:
            click.echo(utils.to_json(data, errors))

        return

    cols = ['id', 'name', 'hostname', 'region', 'type', 'cpu', 'storage', 'memory', 'status', 'host', 'attached_volume']

    table_data = pd.DataFrame(data, index=[0])
    table_data = table_data[[col for col in cols if col in table_data.columns]]

    if len(table_data) > 20:
        click.echo_via_pager(utils.to_table(table_data))
    else:
        click.echo(utils.to_table(table_data))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def modify_instance(options):

    endpoint = f"/instance/{options.first('id')}"

    payload = {
        'name': options['name'][0]
    }

    data, errors = remote.api.patch(endpoint, json=payload)

    if options.get("raw"):
        if not data:
            click.echo("\n[]")
        else:
            click.echo(utils.to_json(data, errors))

        return

    cols = ['id', 'name', 'hostname', 'region', 'type', 'cpu', 'storage', 'memory', 'status', 'host', 'attached_volume']

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

    endpoint = f"/instance/{options.first('id')}/detach"

    data, errors = remote.api.patch(endpoint)

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))

    click.echo(f"Volume has been successfully defatched from instance {options.first('id')}")



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



def delete_instance(options):

    endpoint = f"/instance/{options.first('id')}"

    data, errors = remote.api.delete(endpoint)

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))

    utils.success_response(
        f"Instance {options.first('id')} has been deleted successfully. ")


def jupyter(options):

    endpoint = f"/instance/{options.first('id')}"

    data, errors = remote.api.get(endpoint)

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))

    url = f"https://{data['host']}:8888/"

    click.echo(f"Jupyter is running at: {url}")
    click.launch(url)


def vscode(options):

    endpoint = f"/instance/{options.first('id')}"

    data, errors = remote.api.get(endpoint)

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))

    url = f"https://{data['host']}:8080/"

    click.echo(f"VS Code is running at: {url}")
    click.launch(url)

