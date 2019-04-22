import requests
import json

from library.connection import Postgres
from library.database import *

# define DB connection here

conn = Postgres()

def connections(event, context):
    try:
        s = event["body"]

        # replace connection_list here with actual database function call
        connection_list = conn.
        # connection_list = [
        #     {
        #         "UID": 1,
        #         "Organization": 1,
        #         "Name": "SF",
        #         "CreatedDate": "2019-03-09 20:42:03",
        #         "CreatedBy": 1,
        #         "Type": "A",
        #         "ConnectionInfo": "{conn string}",
        #     },
        #     {
        #         "UID": 2,
        #         "Organization": 1,
        #         "Name": "CW",
        #         "CreatedDate": "2019-03-10 04:42:03",
        #         "CreatedBy": 1,
        #         "Type": "B",
        #         "ConnectionInfo": "{conn string}",
        #     },
        #     {
        #         "UID": 6,
        #         "Organization": 1,
        #         "Name": "Secure Download",
        #         "CreatedDate": "2019-03-23 20:42:03",
        #         "CreatedBy": 0,
        #         "Type": "F",
        #         "ConnectionInfo": 0,
        #     },
        # ]
        payload = json.dumps(connection_list)

    except Exception as e:
        # TODO: Rethink what to return...dumping exceptions is scary for data leakage
        return {"statusCode": 400, "body": "400 Bad Request\n\n" + json.dumps(str(e))}
    return {"statusCode": 200, "body": payload}
