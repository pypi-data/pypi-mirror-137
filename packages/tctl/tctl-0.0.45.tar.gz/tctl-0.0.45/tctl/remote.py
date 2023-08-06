import sys
import os
import requests
from requests.exceptions import ConnectionError
import click

from . import utils, upgrade
from . import credentials
from .version import version
from .env import BASE_URL


def _parse_response(response_obj, halt_on_error=True):
    # "no content" response
    if not response_obj.headers.get('Content-Type') and \
            response_obj.status_code in [201, 202, 204]:
        return None, None

    data = {}
    try:
        data = response_obj.json()
    except Exception:
        click.echo("ERROR: Malformed data returned")
        sys.exit()

    if halt_on_error and int(response_obj.status_code / 100) != 2:
        error = data.get("errors", [{
            "id": "invalid_request",
            "message": "Cannot process request"
        }])[0]

        click.echo(click.style("\nFAILED", fg="red"), nl=False)
        click.echo(" (status code {code}):".format(
            code=response_obj.status_code))

        click.echo(utils.to_json(error))
        sys.exit()

    # if not data.get("data"):
    #     return data

    return data.get("data", {}), data.get("errors", {})


def bearer_token(ver_check=True):
    if ver_check:
        upgrade.check_for_new_version()

    token = os.getenv("TOKEN")
    if not token:
        credentials.config()
    token = utils.decrypt(token)
    return {"Authorization": "Bearer {token}".format(token=token)}


def full_url(endpoint):
    if "http://" in endpoint or "https://" in endpoint:
        return endpoint
    return "{url}/{endpoint}".format(
        url=BASE_URL.strip('/'), endpoint=endpoint.strip('/'))


class api:

    @staticmethod
    def get(endpoint, halt_on_error=True, ver_check=True, **kwargs):
        if "headers" not in kwargs:
            kwargs["headers"] = bearer_token(ver_check)
        kwargs["headers"]["TGX-CLIENT"] = f"tctl {version}"

        try:
            r = requests.get(full_url(endpoint), **kwargs)
            return _parse_response(r, halt_on_error)
        except ConnectionError:
            click.echo("ERROR: Cannot establish connection to Tradologics")
            sys.exit()

    @staticmethod
    def post(endpoint, halt_on_error=True, ver_check=True, **kwargs):
        try:
            if "headers" not in kwargs:
                kwargs["headers"] = bearer_token(ver_check)
            if "timeout" not in kwargs:
                kwargs["timeout"] = 180

            r = requests.post(full_url(endpoint), **kwargs)
            return _parse_response(r, halt_on_error)
        except ConnectionError:
            click.echo("ERROR: Cannot establish connection to Tradologics")
            sys.exit()

    @staticmethod
    def patch(endpoint, halt_on_error=True, ver_check=True, **kwargs):
        try:
            if "headers" not in kwargs:
                kwargs["headers"] = bearer_token(ver_check)
            if "timeout" not in kwargs:
                kwargs["timeout"] = 2

            r = requests.patch(full_url(endpoint), **kwargs)
            return _parse_response(r, halt_on_error)
        except ConnectionError:
            click.echo("ERROR: Cannot establish connection to Tradologics")
            sys.exit()

    @staticmethod
    def put(endpoint, halt_on_error=True, ver_check=True, **kwargs):
        try:
            if "headers" not in kwargs:
                kwargs["headers"] = bearer_token(ver_check)
            if "timeout" not in kwargs:
                kwargs["timeout"] = 2

            r = requests.put(full_url(endpoint), **kwargs)
            return _parse_response(r, halt_on_error)
        except ConnectionError:
            click.echo("ERROR: Cannot establish connection to Tradologics")
            sys.exit()

    @staticmethod
    def delete(endpoint, halt_on_error=True, ver_check=True, **kwargs):
        try:
            if "headers" not in kwargs:
                kwargs["headers"] = bearer_token(ver_check)
            if "timeout" not in kwargs:
                kwargs["timeout"] = 2
            r = requests.delete(full_url(endpoint), **kwargs)
            return _parse_response(r, halt_on_error)
        except ConnectionError:
            click.echo("ERROR: Cannot establish connection to Tradologics")
            sys.exit()

    @staticmethod
    def options(endpoint, halt_on_error=True, ver_check=True, **kwargs):
        try:
            if "headers" not in kwargs:
                kwargs["headers"] = bearer_token(ver_check)
            if "timeout" not in kwargs:
                kwargs["timeout"] = 2

            r = requests.options(full_url(endpoint), **kwargs)
            return _parse_response(r, halt_on_error)
        except ConnectionError:
            click.echo("ERROR: Cannot establish connection to Tradologics")
            sys.exit()

    @staticmethod
    def head(endpoint, halt_on_error=True, ver_check=True, **kwargs):
        try:
            if "headers" not in kwargs:
                kwargs["headers"] = bearer_token(ver_check)
            if "timeout" not in kwargs:
                kwargs["timeout"] = 2

            r = requests.head(full_url(endpoint), **kwargs)
            return _parse_response(r, halt_on_error)
        except ConnectionError:
            click.echo("ERROR: Cannot establish connection to Tradologics")
            sys.exit()
