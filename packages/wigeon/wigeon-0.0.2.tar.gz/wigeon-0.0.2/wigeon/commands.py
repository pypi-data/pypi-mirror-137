# standard imports
from argparse import ArgumentParser
import pathlib as pl
from typing import List
import json
import getpass
import datetime

# external imports
import typer # using for quick build of cli prototype

# project imports
from wigeon.packages import Package
from wigeon.db import Connector, Migration

#################################
## Module level variables
#################################
app = typer.Typer()
user = getpass.getuser()

#################################
## Module level functions
#################################



#################################
## CLI Commands
#################################
@app.command()
def createpackage(
    packagename: str,
    dbtype: str,
    environments: str="local,dev,qa,prod"
):
    """
    createpackage initializes a package of migrations in the current
    environment. A package is linked directly to a database type and the
    deployment environments in your ci/cd pipeline.
    """
    typer.echo(f"Creating {packagename} package")
    typer.echo(f"{packagename}'s Database type is {dbtype}")
    typer.echo(f"{packagename}'s environments include {environments.split(',')}")
     # check if package exists
    package = Package(packagename=packagename)
    package.exists(
        packagename=packagename,
        raise_error_on_exists=True,
        raise_error_on_not_exist=False
    )

    # initialize package folder
    package.create(
        env_list=environments.split(","),
        db_engine=dbtype
    )


@app.command()
def createmigration(
    migrationname: str,
    packagename: str,
    build: str
):
    """
    createmigration initializes a .sql module for a migration
    """
    typer.echo(f"Creating {migrationname} in {packagename} package...")
    # check if package exists
    package = Package(packagename=packagename)
    package.exists()
    # find latest migration number
    current_migrations = package.list_migrations()
    current_migr_num = package.find_current_migration(migration_list=current_migrations)
    typer.echo(f"Current migration is: {current_migr_num}")
    # create migration
    package.add_migration(
        current_migration=current_migr_num,
        migration_name=migrationname,
        builds=[build] # TODO enable multiple build support at later date
    )
    typer.echo(f"Successfully created {current_migr_num}-{migrationname}.sql!!")

@app.command()
def listmigrations(
    packagename: str
):
    """
    listmigrations lists out all migrations for a given package name
    """
    # check if package exists
    package = Package(packagename=packagename)
    package.exists()
    typer.echo(f"Found following migrations for {packagename}:")
    current_migrations = package.list_migrations()
    for m in sorted(current_migrations):
        typer.echo(f"    {m.name}")
    current_migr = package.find_current_migration(migration_list=current_migrations)
    typer.echo(f"Current migration would be: {current_migr}")

@app.command()
def connect(
    packagename: str,
    server: str=None,
    database: str=None,
    username: str=None,
    password: str=None,
    driver: str=None,
    connstring: str=None
):
    """
    connects to a database
    """
    # check if package exists
    package = Package(packagename=packagename)
    package.exists()
    package.read_manifest()
    # create connection, return cursor
    cnxn = Connector(db_engine=package.manifest["db_engine"])
    cur = cnxn.connect(
        server=server,
        database=database,
        username=username,
        password=password,
        driver=driver,
        connstring=connstring
    )
    typer.echo(f"Successfully connected to {package.manifest['db_engine']} database!!!!")

@app.command()
def runmigrations(
    packagename: str,
    server: str=None, # connection variable
    database: str=None, # connection variable
    username: str=None, # connection variable
    password: str=None, # connection variable
    driver: str=None, # connection variable
    connstring: str=None, # connection variable
    all: bool=True, # migration manifest variable
    buildtag: str=None # migration manifest variable
):
    """
    connects to a database and runs migrations
    """
    # check if package exists and read manifest
    package = Package(packagename=packagename)
    package.exists()
    package.read_manifest()
    # create connection
    connector = Connector(db_engine=package.manifest["db_engine"])
    cnxn = connector.connect(
        server=server,
        database=database,
        username=username,
        password=password,
        driver=driver,
        connstring=connstring
    )
    cur = cnxn.cursor()
    typer.echo(f"Successfully connected to {package.manifest['db_engine']} database!!!!")

    # initialize changelog table if not exists and add columns
    # change_id, migration_date, applied_by(username), and migration_name(.sql filename)
    query_create_changelog = """
    CREATE TABLE IF NOT EXISTS changelog (change_id INTEGER NOT NULL PRIMARY KEY, migration_date TEXT, migration_name TEXT, applied_by TEXT);
    """
    cur.execute(query_create_changelog)
    cnxn.commit()
    
    # find migrations already in target database
    query_migrations_from_changelog = """
    SELECT migration_name from changelog
    """
    cur.execute(query_migrations_from_changelog)
    db_migrations = [n[0] for n in cur.fetchall()]

    # find migrations in manifest
    # filter to migrations only with certain build tag
    mani_migrations = [Migration(**m) for m in package.fetch_manifest_migrations(buildtag=buildtag)]

    # run migrations if not already in db
    duplicate_migrations = [m.name for m in mani_migrations if m.name in db_migrations]
    print(f"Migrations already in db: {duplicate_migrations}")
    mani_migrations = [m for m in mani_migrations if m.name not in db_migrations]
    print(f"Migrations to run: {mani_migrations}")
    for mig in mani_migrations:
        if mig.name in db_migrations:
            duplicate_migrations.append(mig.name)
            continue
        mig.run(
            package=package,
            cursor=cur,
            user=user
        )
    print(f"Successfully ran {len(mani_migrations)} migrations")
    cnxn.commit()
    cnxn.close()

if __name__ == "__main__":
    app()