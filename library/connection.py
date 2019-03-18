# functions for converting from sql query results to JSON for API
# ie: SQL Results <-> JSON conversions


class Connection:
    """For subclassing to create new connections to databases
    
    """

    def __init__(self, *args, **kwargs):
        pass

    def query(self, query: str):
        """Make query to database
        
        Parameters
        ----------
        query : str
            SQL query string
        
        """

        pass
