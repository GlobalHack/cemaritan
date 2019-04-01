# functions for converting from sql query results to JSON for API
# ie: SQL Results <-> JSON conversions
import os

import sqlite3
import psycopg2


class SQLite:
    def __init__(self, db_path, *args, **kwargs):
        self._db_path = db_path
        self.connection = sqlite3.connect(self._db_path)

    def query(self, query: str):
        """[summary]
        
        Parameters
        ----------
        query : str
            [description]
        
        """
        try:
            response = self.connection.execute(query)
            self.connection.commit()
            return response
        except Exception as e:
            print(e)


class Postgres:
    def __init__(self, db_path, *args, **kwargs):
        self._host = os.environ["POSTGRES_HOST"]
        self._database = os.environ["POSTGRES_DATABASE"]
        self._user = os.environ["POSTGRES_USER"]
        self._password = os.environ["POSTGRES_PASSWORD"]
        # TODO: Update this connection
        self.connection = None

        # TODO: bool for whether connection is open or not

    def connection(self):
        """Returns connection if still open, else opens a new 
        connection and returns it
        
        Returns
        -------
        Connection
            Connection to Postgres database
        """

        try:  # test for open connection
            c = self.connection.cursor()
            c.execute("SELECT 1")
            return self.connection
        except:
            self.connection = psycopg2.connection(
                host=self._host,
                database=self._database,
                user=self._user,
                password=self._password,
            )
            return self.connection

    def query(self, query: str):
        """Submit query to database
        
        Parameters
        ----------
        query : str
            SQL statement to execute
        
        """
        try:
            c = self.connection.cursor()
            response = c.execute(query)
            c.commit()
            c.close()
            return response
        except Exception as e:
            print(e)
