import click
import uvicorn

from setups.config import AppConfig


@click.command()
@click.option("--debug", is_flag=True)
def cli(debug: bool):
    """
        Run application.
    """

    try:
        uvicorn.run(
            "setups.app:app", host=AppConfig.HOST, port=AppConfig.PORT, reload=debug
        )
    except ValueError as e:
        click.echo(e.args[0])


if __name__ == "__main__":
    cli()
