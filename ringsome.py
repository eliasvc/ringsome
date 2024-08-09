import subprocess
import sys
import requests
import click
from rich.console import Console
from rich.table import Table

import countrycodes

BASE_URL = "https://api.ring.nlnog.net/1.0"


@click.group()
def cli():
    pass


@cli.group()
def get():
    pass


@get.command()
def countries():
    r = requests.get(BASE_URL + "/countries")
    if r.status_code != 200:
        r.raise_for_status()
    table = Table(title="Ring Countries")
    table.add_column("Country Code", justify="center")
    table.add_column("Country Name", justify="left")
    for code in r.json()["results"]["countrycodes"]:
        table.add_row(code, countrycodes.alpha2[code])
    console = Console(emoji=False)
    console.print(table)


@get.command()
@click.option("--country", help="Alpha-2 country code")
def nodes(country):
    if country:
        r = requests.get(BASE_URL + f"/nodes/active/country/{country}")
    else:
        r = requests.get(BASE_URL + "/nodes/active")
    if r.status_code != 200:
        r.raise_for_status()
    result = r.json()["results"]["nodes"]
    # Sort by country
    result = sorted(result, key=lambda node: node["countrycode"])
    table = Table(title="Ring Nodes")
    table.add_column("Hostname", justify="left")
    table.add_column("IPv4")
    table.add_column("IPv6")
    table.add_column("Country")
    table.add_column("City")
    for node in result:
        table.add_row(
            node["hostname"],
            node["ipv4"],
            node["ipv6"],
            node["countrycode"],
            "Null" if node["city"] == "" else node["city"],
        )
    console = Console(emoji=False)
    console.print(table)


def ssh(user, host, command, port=22):
    output = subprocess.run(["ssh", f"{user}@{host}", "-p", f"{port}", command])
    return output


@cli.command()
@click.option("--host", type=str, help="Target hostname or IP. Requires --user")
@click.option("--user", type=str, help="SSH user to be used in connection")
@click.option(
    "--port",
    type=str,
    default=22,
    show_default=True,
    help="Port to be used in SSH connection. Default is 22",
)
@click.option(
    "--command", required=True, type=str, help="Command to execute in target host"
)
def run(host, user, command, port):
    """Run commmand on specified host or on a random number of Ring hosts from a specified country"""
    if host and not user:
        print(
            "Usage: ringsome.py run [OPTIONS]\n"
            "Try 'ringsome.py run --help' for help.\n\n"
            "Error: '--host' requires '--user'."
        )
        sys.exit(2)
    elif host:
        output = ssh(user, host, command, port)
        if output.returncode == 0:
            print(output.stdout)


def main():
    cli()


if __name__ == "__main__":
    main()
