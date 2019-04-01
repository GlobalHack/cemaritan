import requests

from library.connection import Aurora
from library.database import *

# define DB connection here


def connections(event, context):
    try:
        s = event["body"]

        get_connections()
        connection_list = ["org1", "org2"]

    except Exception as e:
        # TODO: Rethink what to return...dumping exceptions is scary for data leakage
        return {"statusCode": 400, "body": "400 Bad Request\n\n" + json.dumps(str(e))}
    return {"statusCode": 200, "body": connection_list}
