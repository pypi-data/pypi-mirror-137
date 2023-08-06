# standard imports
import pathlib as pl
import sqlite3
import pyodbc

# external imports

# project imports


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