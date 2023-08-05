"""This module defines the CLI for alias_cd."""

import os
import functools
import typer

import alias_cd
from alias_cd import config

app = typer.Typer()
CONFIG = None
DEFAULT_LABEL = "<DEFAULT>"


def validate_config_initilized(func):
    """Decotate function to validate CONFIG is correctly initilized."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if isinstance(CONFIG, config.Config):
            return func(*args, **kwargs)
        else:
            typer.secho("Config not initilized", fg=typer.colors.RED, err=True)
            exit(-1)

    return wrapper


@app.command(name="get")
@validate_config_initilized
def get(name: str):
    """Display the directory for the given directory."""

    if CONFIG.has_aias(name):  # type: ignore # validate_config_initilized checks this
        typer.echo(CONFIG.get_directory(name))  # type: ignore
    else:
        typer.secho(f"alias {name} not found", fg=typer.colors.RED, err=True)
        exit(-1)


@app.command()
def version():
    """Display the version of the CLI."""

    typer.echo(alias_cd.__version__)


@app.command(name="list")
@validate_config_initilized
def list():
    """Display all stored aliases."""

    padding_size = max(
        max(
            [
                len(alias) if alias is not None else len(DEFAULT_LABEL)
                for alias in CONFIG.aliases
            ]
        ),
        5,
    )
    typer.echo(f"{'Alias':{padding_size}} | Directory")
    for alias, directory in CONFIG.aliases.items():
        if alias is None:
            alias = DEFAULT_LABEL
        typer.echo(f"{alias:{padding_size}} | {directory}")


@app.command(name="validate")
@validate_config_initilized
def validate():
    """Check that all aliases are valid."""

    exit_status = 0

    for alias in CONFIG.aliases:  # type: ignore
        directory = CONFIG.get_directory(alias)  # type: ignore
        if not os.path.exists(directory):
            exit_status = -1
            typer.secho(
                f"invalid {alias=} {directory=} does not exist.",
                fg=typer.colors.RED,
                err=True,
            )

    exit(exit_status)


@app.callback()
def _global_init(config_path: str = None):
    try:
        global CONFIG
        CONFIG = config.load_config(config_path)
    except ValueError as err:
        typer.secho(err, fg=typer.colors.RED, err=True)
        exit(-1)


if __name__ == "__main__":
    app()
