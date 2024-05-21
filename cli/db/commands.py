import click
import sqlite3
from cfg import cfg


ptwildlife_db = cfg.root / "containers/PytorchWildlife/data/wildlife.db"


@click.group(name="db", help="Run various db functions")
def db():
    pass


@db.command(name="delete", help="Delete tables")
@click.option("--table", "-t", help="Tables to delete", multiple=True)
def deletetables(table: list[str]):
    conn = sqlite3.connect(ptwildlife_db)
    curr = conn.cursor()
    for t in table:
        click.echo(f"Deleting table {t}...")
        curr.execute(f"DROP TABLE IF EXISTS {t};")
    conn.commit()
    conn.close()

@db.command(name="deletedata", help="Delete data")
@click.option("--table", "-t", help="Table to delete data from", multiple=True)
def deletedata(table: list[str]):
    conn = sqlite3.connect(ptwildlife_db)
    curr = conn.cursor()
    for t in table:
        click.echo(f"Deleting data from table {t}...")
        curr.execute(f"DELETE FROM {t};")
    conn.commit()
    conn.close()

@db.command(name="showtables", help="Show tables")
def showtables():
    conn = sqlite3.connect(ptwildlife_db)
    curr = conn.cursor()
    curr.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = curr.fetchall()
    for t in tables:
        click.echo(t[0])
    conn.close()
