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
    def __init__(self, db_path: str = None, *args, **kwargs):
        self._host = os.environ["host"]
        self._port = os.environ["port"]
        self._database = os.environ["dbname"]
        self._user = os.environ["user"]
        self._password = os.environ["pw"]
        self._connection = self.create_new_connection()

        # TODO: bool for whether connection is open or not

    def create_new_connection(self):
        return psycopg2.connect(
            host=self._host,
            port=self._port,
            database=self._database,
            user=self._user,
            password=self._password,
        )

    def connection(self):
        """Returns connection if still open, else opens a new 
        connection and returns it
        
        Returns
        -------
        Connection
            Connection to Postgres database
        """

        try:  # test for open connection
            c = self._connection.cursor()
            c.execute("SELECT 1")
            return self._connection
        except:
            self._connection = self.create_new_connection()
            return self._connection

    def query(self, query: str):
        """Submit query to database
        
        Parameters
        ----------
        query : str
            SQL statement to execute
        
        """
        try:
            c = self._connection.cursor()
            response = c.execute(query)
            c.close()
            return response
        except Exception as e:
            print(e)
