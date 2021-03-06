# functions for converting from sql query results to JSON for API
# ie: SQL Results <-> JSON conversions
import os
from typing import Any, List, Tuple

import psycopg2

# Only need sqlite3 for local testing
try:
    import sqlite3
except:
    pass
    

def zip_column_names_and_rows(
    column_names: List[str], rows: List[Tuple]
) -> List[List[Tuple[str, Any]]]:
    """Returns list of List of 2-tuples of `column_name`, `row`
    
    Parameters
    ----------
    column_names : List[str]
        Column names
    rows : List[Tuple]
        List of tuples representing rows
    
    Returns
    -------
    List[List[Tuple[str, Any]]]
        List of List of 2-tuples representing each row of the response of the query
        Example: 
        [
            (
                ("uid", 1),
                ("organization", 1),
                ("name", "SF"),
                ("created_datetime", "2019-03-09 20:42:03"),
                ("created_by", 1),
                ("type", "A"),
                ("connection_info", "{conn string}")
            ),
            (
                ("uid", 2),
                ("organization", 1),
                ("name", "CW"),
                ("created_datetime", "2019-03-10 04:42:03"),
                ("created_by", 1),
                ("type", "B"),
                ("connection_info", "{conn string}")
            )
        ]

    """
    labeled_rows = []
    for row in rows:
        new_row = tuple(zip(column_names, row))
        labeled_rows.append(new_row)
    return labeled_rows


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
        self._host = os.environ["DB_HOST"]
        self._port = os.environ["PORT"]
        self._database = os.environ["DB_NAME"]
        self._user = os.environ["USER"]
        self._password = os.environ["PASSWORD"]
        self._connection = self.create_new_connection()

        # TODO: bool for whether connection is open or not

    def create_new_connection(self):
        conn = psycopg2.connect(
            host=self._host,
            port=self._port,
            database=self._database,
            user=self._user,
            password=self._password,
        )
        conn.autocommit = True
        return conn

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

    def query(self, query: str, null_return: bool=False):
        """Submit query to database
        
        Parameters
        ----------
        query : str
            SQL statement to execute
        
        """
        try:
            c = self.connection().cursor()  # was self._connection.cursor()
            c.execute(query)
            if null_return:
                return
            column_names = [x.name for x in c.description]
            rows = list(c.fetchall())  # limit to 100 results in the future?
            to_return = zip_column_names_and_rows(column_names, rows)
            return to_return
        except Exception as e:
            print(str(type(e)) + str(e))
            self._connection.rollback()
        finally:
            c.close()


def get_conn(name: str='postgres'):
    if name=='postgres':
        return Postgres()