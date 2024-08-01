import requests
import click
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
    print("Getting countries")


@get.command()
def nodes():
    print("Getting nodes")


def main():
    cli()
    r = requests.get(BASE_URL + "/countries")
    if r.status_code != 200:
        r.raise_for_status()
    print(r.json()["results"]["countrycodes"])


if __name__ == "__main__":
    main()
