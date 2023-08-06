#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import click
from .. import utils
from .. import remote
from decimal import Decimal
import pandas as pd
pd.options.display.float_format = '{:,}'.format


def positions_list(options):

    connection = options.first("connection")

    endpoint = "/positions"
    payload = {}

    if connection:
        endpoint = "/connection/{connection}/positions".format(connection=connection)
    if options.get("strategy"):
        payload["strategies"] = options.get("strategy")
    if options.get("start"):
        payload["date_from"] = options.get("start")
    if options.get("end"):
        payload["date_to"] = options.get("end")
    if options.get("status"):
        payload["statuses"] = options.get("status")

    if payload:
        data, errors = remote.api.get(endpoint, json=payload)
    else:
        data, errors = remote.api.get(endpoint)

    if options.get("raw"):
        if not data:
            click.echo("\n[]")
        else:
            click.echo(utils.to_json(data, errors))
        return

    if not data:
        click.echo("\nNo positions found.")
        return

    if not connection:
        # display count
        count = 0
        rows = []
        for conn, positions in data.items():
            ln = len(positions)
            count += ln
            rows.append({
                "connection": conn,  # connections.get(conn, conn),
                "positions": ln
            })
        if count == 0:
            click.echo("\nNo positions found.")
            return

        click.echo(utils.to_table(rows))

    else:
        rows = []
        for item in data:
            item['currency'] = item['asset']['currency']
            item['asset'] = f"{item['asset']['ticker']}:{item['asset']['region']}"
            rows.append(item)

        df = pd.DataFrame(rows)

        df = df[[
            'start_date', 'end_date', 'asset', 'qty',
            'side', 'avg_fill_price', 'last_price',
            'pnl', 'pnl_pct', 'currency'
        ]]

        df.rename(columns={
            'start_date': 'from',
            'end_date': 'to',
            'strategy_id': 'strategy',
            'connection_id': 'connection',
            'limit_price': 'price',
        }, inplace=True)

        df["side"] = df["side"].str.upper()
        df['from'] = pd.to_datetime(
            df['from']).dt.strftime('%Y-%m-%d %H:%M:%S')
        df['to'] = pd.to_datetime(
            df['to']).dt.strftime('%Y-%m-%d %H:%M:%S')

        for col in df.columns:
            if "_pct" in col:
                df[col] = df[col].astype(float) * 100

        df['qty'] = df['qty'].apply(lambda x: "{:,.0f}".format(int(x)))
        df.columns = [col.replace("_", " ").title() for col in df.columns]

        if len(df) > 20:
            click.echo_via_pager(utils.to_table(df))
        else:
            click.echo(utils.to_table(df))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))


def position_orders_list(options):
    if "position" not in options:
        click.echo('\nMissing required flag: [--position|-p  {POSITION_ID}]')
        return

    position_id = options.first("position")
    endpoint = f"/position/{position_id}/orders"

    payload = {}

    if payload:
        data, errors = remote.api.get(endpoint, json=payload)
    else:
        data, errors = remote.api.get(endpoint)

    if options.get("raw"):
        if not data:
            click.echo("\n[]")
        else:
            click.echo(utils.to_json(data, errors))
        return

    if not data:
        click.echo(f"No order found for trade {position_id}")
    else:
        data = data[position_id]
        rows = []
        for row in data:
            for col in ['qty', 'filled_qty', 'avg_fill_price']:
                row[col] = utils.to_decimal(row[col])

            row["currency"] = row['asset']['currency']
            row["asset"] = f"{row['asset']['ticker']}:{row['asset']['region']}"
            row["filled"] = f"{row['filled_qty']}/{row['qty']}"

            row["status"] = row["status"].title()
            row["side"] = row["side"].title()
            row["type"] = {
                'market': 'MKT',
                'limit': 'LMT',
                'stop': 'STP',
                'stop_limit': 'STP LMT',
            }.get(row["type"], row["type"])
            row["tif"] = row["tif"].upper()

            rows.append(row)

        cols = [
            'asset', 'filled',
            'side', 'type', 'tif',
            'limit_price', 'stop_price'
            'avg_fill_price', 'status',
            'created_at', 'updated_at',
            'comment', 'strategy_id',
            'connection_id', 'currency']

        if options.first('ids', False):
            cols = ['order_id'] + cols

        df = pd.DataFrame(rows)
        df = df[[col for col in cols if col in df.columns]]

        df.rename(columns={
            'created_at': 'created',
            'updated_at': 'updated',
            'strategy_id': 'strategy',
            'connection_id': 'connection',
            'limit_price': 'price',
        }, inplace=True)

        df['created'] = pd.to_datetime(
            df['created']).dt.strftime('%Y-%m-%d %H:%M:%S')
        df['updated'] = pd.to_datetime(
            df['updated']).dt.strftime('%Y-%m-%d %H:%M:%S')

        df.columns = [
            col.replace("_", " ").title() for col in df.columns]

        if len(df) > 20:
            click.echo_via_pager(utils.to_table(df))
        else:
            click.echo(utils.to_table(df))

    if errors:
        click.echo("\nErrors:")
        click.echo(utils.to_table(errors))

