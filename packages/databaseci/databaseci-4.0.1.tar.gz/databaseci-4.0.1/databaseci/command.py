import json
from pathlib import Path

import click
import yaml

from .do import do_check, do_copy, do_inspect


@click.group()
def cli():
    pass


@cli.command()
@click.argument("file", type=click.Path(exists=True), nargs=1)
def copy(file):
    with Path(file).open() as f:

        j = yaml.safe_load(f)
    do_copy(j)


@cli.command()
@click.argument("file", type=click.Path(exists=True), nargs=1)
def inspect(file):
    with Path(file).open() as f:

        j = yaml.safe_load(f)
    do_inspect(j)


@cli.command()
@click.argument("file", type=click.Path(exists=True), nargs=1)
def check(file):
    with Path(file).open() as f:

        j = yaml.safe_load(f)
    do_check(j)
