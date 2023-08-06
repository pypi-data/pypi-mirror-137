# standard imports
import pathlib as pl
import sqlite3
import datetime
from typing import Union, List

# external imports
import pyodbc

# project imports
from wigeon.packages import Package


class Connector(object):
    db_engines = [
        "sqlite",
        "mssql",
        "postgres"
    ]

    def __init__(self, db_engine: str):
        self.db_engine = db_engine
        self.cnxn = None

    def connect(
        self,
        **kwargs
    ):
        db_engines = {
            "sqlite": self.conn_sqlite,
            "mssql": self.conn_mssql,
            "postgres": self.conn_postgres
        }
        # run connection method based on db_engine for package
        db_engines[self.db_engine](**kwargs)
        return self.cnxn
        

    def conn_sqlite(
        self,
        **kwargs
    ) -> sqlite3.Connection:
        """
        Connect to a sqlite database and return conn
        """
        self.cnxn = sqlite3.connect(kwargs["connstring"])

    def conn_mssql(self, **kwargs):
        raise NotImplementedError("conn_mssql is not yet implemented!")
    
    def conn_postgres(self, **kwargs):
        raise NotImplementedError("conn_postgres is not yet implemented!")

class Migration(object):

    def __init__(
        self,
        name: str,
        builds: List[str]
    ):
        self.name = name
        self.builds = builds
    
    def __str__(self):
        return f"name: {self.name}, builds: {self.builds}"
    
    def __repr__(self):
        return f"name: {self.name}, builds: {self.builds}"

    def run(
        self,
        package: Package,
        cursor: Union[sqlite3.Cursor, pyodbc.Cursor],
        user: str
    ):
        with open(package.pack_path.joinpath(self.name), "r") as f:
            query = f.read()
        cursor.execute(query)
        cursor.execute(
            "INSERT INTO changelog (migration_date, migration_name, applied_by) VALUES(:migration_date, :migration_name, :applied_by)",
            {
                "migration_date": datetime.datetime.now().strftime("%Y%m%d-%H%M"),
                "migration_name":self.name,
                "applied_by": user
            }
        )