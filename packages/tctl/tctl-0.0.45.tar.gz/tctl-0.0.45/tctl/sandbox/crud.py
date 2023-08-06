#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import sys
import click
from .. import utils
from .. import remote
import requests
import pandas as pd


def tradehook(event, url):
    """
    authorization required
    Parameters
    ----------
    kind : available kinds: ["bar", "order", "order_{YOUR_STATUS}  (example: "order_filled")", "position",
    "position_expire", "price", "price_expire", "error"]
    strategy : callback
    kwargs : payload
    Returns
    -------
    json obj
    """

    data = remote.api.get(
        f"/sandbox/{event.replace('_', '/')}", **utils.argv_kwargs())

    # build payload
    payload = {
        "event": event.split('_')[0],
        "data": data
    }

    # send payload to url
    response = requests.post(url, json=payload)
    click.echo(f"Server replied with {response.status_code} code")

    # print(utils.to_table(
    #     pd.DataFrame(dict(response.headers), index=[0]).T.reset_index(),
    #     showheaders=False,
    #     tablefmt="plain"
    # ), "\n")

    if 'application/json' in response.headers.get('Content-Type'):
        data = response.json()
        if data:
            print("\nServer response")
        click.echo(utils.to_json(data))
        return

    if response.text:
        print("\nServer response")
        click.echo(response.text)
        return

    click.echo("[no content]")


# def positions_list(options):
def sandbox_bar(options):
    url = options.first('url')
    if not utils.is_valid_uri(url):
        click.echo("\nERROR: `{}` is not a valid URL.".format(url))
        sys.exit()
    tradehook("bar", url)


def sandbox_position(options):
    url = options.first('url')
    if not utils.is_valid_uri(url):
        click.echo("\nERROR: `{}` is not a valid URL.".format(url))
        sys.exit()

    if options.first('expired'):
        tradehook("position_expire", url)
    else:
        tradehook("position", url)


def sandbox_price(options):
    url = options.first('url')
    if not utils.is_valid_uri(url):
        click.echo("\nERROR: `{}` is not a valid URL.".format(url))
        sys.exit()

    if options.first('expired'):
        tradehook("price_expire", url)
    else:
        tradehook("price", url)


def sandbox_error(options):
    url = options.first('url')
    if not utils.is_valid_uri(url):
        click.echo("\nERROR: `{}` is not a valid URL.".format(url))
        sys.exit()
    tradehook("error", url)


def sandbox_order(options):
    url = options.first('url')
    if not utils.is_valid_uri(url):
        click.echo("\nERROR: `{}` is not a valid URL.".format(url))
        sys.exit()

    kinds = [
        "received",
        "pending",
        "submitted",
        "sent",
        "accepted",
        "partially_filled",
        "filled",
        "canceled",
        "expired",
        "pending_cancel",
        "rejected"
    ]
    kind = options.first('kind')
    if kind not in kinds:
        click.echo("\nERROR: kind should be one of: {}.".format(kinds).replace('[', '').replace(']', '').replace("'", '`'))
        sys.exit()

    tradehook(f"order_{kind}", url)
