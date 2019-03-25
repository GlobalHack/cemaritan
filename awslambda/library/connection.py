# functions for converting from sql query results to JSON for API
# ie: SQL Results <-> JSON conversions
import sqlite3


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
