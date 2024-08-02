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
    r = requests.get(BASE_URL + "/countries")
    if r.status_code != 200:
        r.raise_for_status()
    for code in r.json()["results"]["countrycodes"]:
        print(f"{code}\t{countrycodes.alpha2[code]}")


@get.command()
def nodes():
    print("Getting nodes")


def main():
    cli()


if __name__ == "__main__":
    main()
