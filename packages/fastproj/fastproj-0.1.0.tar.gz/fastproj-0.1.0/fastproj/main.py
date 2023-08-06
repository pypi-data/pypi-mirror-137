from pathlib import Path

import typer
from loguru import logger

import fastproj

app = typer.Typer()


@app.command()
def init() -> None:
    proj = Path(fastproj.__file__).parent

    for one in proj.glob('**/*'):
        logger.debug(one)


@app.command()
def buy() -> None:
    typer.echo(f"what")


def run() -> None:
    return app()


if __name__ == "__main__":
    run()
