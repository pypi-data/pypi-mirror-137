#!/usr/bin/env python

import click
# import ujson
from .. import utils
from .. import inputs
from .. import remote
from decimal import Decimal
import sys
import pandas as pd
pd.options.display.float_format = '{:,}'.format

OAUTH_BROKERS = ["ib"]

NUMERIC_COLS = ["regt_buying_power", "equity", "daytrading_buying_power",
                "buying_power", "cash", "unrealized_pnl", "realized_pnl",
                "initial_margin", "maintenance_margin", "sma"]


def connections_list(options):
    data, errors = remote.api.get("/connections")

    for x in data:
        if "realized_pnl" not in data[x]:
            data[x]["realized_pnl"] = 0
        if "unrealized_pnl" not in data[x]:
            data[x]["unrealized_pnl"] = 0
        if "equity" not in data[x]:
            data[x]["equity"] = 0

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    if not data:
        click.echo("\nNo connections found.")
        return

    table_data = []
    for x in data:
        item = {
            "name": data[x]["name"],
            "id": data[x]["connection_id"],
            "broker": "{broker} ({currency})".format(
                broker=data[x]["broker"].title(),
                currency=data[x]["currency"]
            ),
            "is_paper": data[x]["paper"],
            "equity": utils.fillna(data[x]["equity"], True),
            "realized_pnl": utils.fillna(data[x]["realized_pnl"], True),
            "unrealized_pnl": utils.fillna(data[x]["unrealized_pnl"], True),
        }

        table_data.append(item)

    click.echo(utils.to_table(table_data))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def connection_info(options):
    data, errors = remote.api.get("/connection/{connection}".format(
        connection=options.first("connection")))

    if "realized_pnl" not in data:
        data["realized_pnl"] = 0
    if "unrealized_pnl" not in data:
        data["unrealized_pnl"] = 0
    if "equity" not in data:
        data["equity"] = 0

    data["broker"] = data["broker"].title()

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    df = pd.DataFrame([data])
    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = utils.fillna(df[col].fillna(0).astype(str).values[0], True)

    # order cols
    df = df[[
        'name',
        'connection_id',
        'broker',
        'account',
        'cash',
        'equity',
        'currency',
        'paper',
        'unrealized_pnl',
        'realized_pnl',
        'status',
        'blocked',
        'buying_power',
        'initial_margin',
        'maintenance_margin',
        'pattern_day_trader',
        'regt_buying_power',
        'daytrading_buying_power',
        'daytrade_count',
        'shorting_enabled',
        'multiplier',
        'sma',
    ]]

    df.columns = [col.replace("_", " ").title() for col in df.columns]
    click.echo(utils.to_table(df.T, showindex=True, showheaders=False))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def connection_create(options):

    brokers = {}
    supported_brokers, errors = remote.api.get("/brokers?tctl=true")
    for broker in supported_brokers:
        brokers[broker['name']] = broker

    click.echo("")
    name = ""
    while name == "":
        name = inputs.text("Account name")

    broker = inputs.option_selector(
        "Please select broker", list(brokers.keys()))
    broker = brokers.get(broker)

    paper_mode = False
    auth = {}
    payload = {}

    if broker["broker_id"] in OAUTH_BROKERS:
        click.echo(f"{broker['name']} used OAuth.\n")
        click.echo("Please connect to this account from the dashboard, at:")
        click.echo("https://cloud.tradologics.com/connections")
        sys.exit(1)

    if broker["name"] == "tradologics":
        paper_mode = True
        payload = utils.virtual_connection_payload("paper")

    else:
        if broker.get("has_paper", False):
            paper_mode = inputs.confirm(
                "Use broker's paper account", default=True)

        # if broker["name"] == "ib":
        #     while not auth.get("key"):
        #         auth["key"] = inputs.text("Username")
        #     while not auth.get("secret"):
        #         auth["secret"] = inputs.hidden("Password")
        #     while not auth.get("connection_id"):
        #         auth["connection_id"] = inputs.hidden("Account ID")
        else:
            for key in broker["auth"]:
                while not auth.get(key):
                    auth[key] = inputs.hidden(
                        key.replace("_", " ").title().replace("Id", "ID"))

    payload = {**payload, **{
        "name": name,
        "paper": paper_mode,
        "auth": auth,
        "broker": broker["broker_id"]
    }}

    data, errors = remote.api.post("/connections", json=payload)

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    utils.success_response(
        f"The account `{name}` ({broker['name']}) is now connected to your Tradologics account.")

    df = pd.DataFrame([data])
    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col])

    df.columns = [col.replace("_", " ").title() for col in df.columns]
    click.echo(utils.to_table(df.T, showindex=True, showheaders=False))

    if broker["name"] == "ib":
        click.echo("\nNOTE:\nIB accounts can take up to 5 minutes to be deployed.")
        click.echo("\nCheck your connection status in a few minutes using")
        click.echo(f"  tctl connections info --connection {data['connection_id']}")


def connection_update(options):

    connection, errors = remote.api.get("/connection/{connection}".format(
        connection=options.first("connection")))

    supported_brokers, errors = remote.api.get("/brokers")
    for broker in supported_brokers:
        if broker["broker_id"] == connection["broker"]:
            break

    click.echo(f"\Broker: {broker['name']}\n")
    name = ""
    while name == "":
        name = inputs.text("Connection name")

    paper_mode = False
    key = secret = connection_id = None

    if broker["broker_id"] == "tradologics":
        paper_mode = True
    else:
        if broker["broker_id"] != "paper":
            if broker.get("has_paper", True):
                paper_mode = inputs.confirm(
                    "Use broker's paper account", default=True)

            click.echo(
                "\nTo update credentials, enter new information (leave blank otherwise):\n")

            if broker["broker_id"] == "ib":
                key = inputs.text("Username")
                secret = inputs.hidden("Password")
                connection_id = inputs.hidden("Account ID")
            else:
                key = inputs.hidden("Key (API key or Token)")
                secret = inputs.hidden("Secret (leave blank if using a token)")

    payload = {
        "name": name,
        "paper": paper_mode
    }

    if key or secret or connection_id:
        payload["auth_info"] = {}
        if key:
            payload["auth_info"]["key"] = key
        if secret:
            payload["auth_info"]["secret"] = secret
        if connection_id:
            payload["auth_info"]["connection_id"] = connection_id

    click.echo(utils.to_json(payload))
    # return

    data, errors = remote.api.patch(f"/connection/{connection['connection_id']}", json=payload)

    if "realized_pnl" not in data:
        data["realized_pnl"] = 0
    if "unrealized_pnl" not in data:
        data["unrealized_pnl"] = 0
    if "equity" not in data:
        data["equity"] = 0

    data["broker"] = data["broker"].title()

    if options.get("raw"):
        click.echo(utils.to_json(data, errors))
        return

    utils.success_response(
        f"The connection `{name}` ({broker['name']}) was updated")

    df = pd.DataFrame([data])
    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = utils.fillna(df[col].fillna(0).astype(str).values[0], True)

    # order cols
    df = df[[
        'name',
        'connection_id',
        'broker',
        'account',
        'cash',
        'equity',
        'currency',
        'paper',
        'unrealized_pnl',
        'realized_pnl',
        'status',
        'blocked',
        'buying_power',
        'initial_margin',
        'maintenance_margin',
        'pattern_day_trader',
        'regt_buying_power',
        'daytrading_buying_power',
        'daytrade_count',
        'shorting_enabled',
        'multiplier',
        'sma',
    ]]

    df.columns = [col.replace("_", " ").title() for col in df.columns]
    click.echo(utils.to_table(df.T, showindex=True, showheaders=False))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def connection_delete(options):
    connection = options.first("connection")
    remote.api.delete("/connection/{connection}".format(
        connection=options.first("connection")))

    utils.success_response(
        f"The connection `{connection}` was removed succesfully.")
