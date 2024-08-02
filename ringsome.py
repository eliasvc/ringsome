import requests
import click
from rich import print as rprint
from rich.table import Table

import countrycodes

BASE_URL = "https://api.ring.nlnog.net/1.0"


@click.group()
def cli():
    pass


@cli.group()
def get():
    click.echo("Get command")


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
    rprint(table)


@get.command()
def nodes():
    print("Getting nodes")


def main():
    cli()


if __name__ == "__main__":
    main()
