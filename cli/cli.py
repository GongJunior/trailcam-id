import logging
import click
from cfg import cfg


@click.group(name="classify", help="Run various cv functions")
def cli():
    pass


def init():
    from sample.commands import sample
    from db.commands import db

    cli.add_command(sample)
    cli.add_command(db)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        encoding="utf-8",
        format="%(levelname)s %(asctime)s: %(message)s",
    )
    init()
    cli()
