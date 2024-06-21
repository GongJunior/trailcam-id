import click
import sqlite3
from cfg import cfg


ptwildlife_db = cfg.root / "containers/PytorchWildlife/app/data/wildlife.db"


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

@db.command(name="seedclassifications", help="Seed ClassNmaeMap with data, error if data already exists")
def seedclassifications():
    conn = sqlite3.connect(ptwildlife_db)
    curr = conn.cursor()
    curr.execute("SELECT * FROM class_name_map;")
    if not curr.fetchall() == []:
        click.echo("Data already exists in class_name_map, use deletedata class_name_map to delete data first.")
        conn.close()
        return
    seed_data = cfg.get_ClassNameMapSeedData()
    for t in seed_data:
        curr.execute("INSERT INTO class_name_map (classifier_name, display_description, display_name) VALUES (?, ?, ?);", (t[0], t[1], t[2]))
    conn.commit()

    rows_added = curr.execute("SELECT COUNT(*) FROM class_name_map;").fetchall()[0][0]
    click.echo(f"Added {rows_added} rows to class_name_map.")

@db.command(name="showsampledata", help="Show sample data from specified table")
@click.option("--table", "-t", help="Table to show sample data from", required=True)
def showsampledata(table: str):
    click.echo(f"Showing sample data from {table}...")
    conn = sqlite3.connect(ptwildlife_db)
    curr = conn.cursor()
    curr.execute(f"SELECT * FROM {table} LIMIT 5;")
    data = curr.fetchall()
    if data == []:
        click.echo(f"No data found in {table}")
        conn.close()
        return
    for d in data:
        click.echo(d)
    conn.close()

@db.command(name="sql", help="Run SQL query")
@click.option("--query", "-q", help="SQL query to run", required=True)
def sql(query: str):
    click.echo(f"Running query: {query}")
    conn = sqlite3.connect(ptwildlife_db)
    curr = conn.cursor()
    curr.execute(query)
    data = curr.fetchall()
    if data == []:
        click.echo("No data found.")
        conn.close()
        return
    for d in data:
        click.echo(d)
    conn.close()