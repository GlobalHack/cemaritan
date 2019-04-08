import requests
import json

from library.connection import Postgres
from library.database import *

# define DB connection here


def organizations(event, context):
    try:
        s = event["body"]

        # replace user_list here with actual database function call
        user_list = [
            {
                "UID": 1,
                "Name": "Matt",
                "CreatedDate": "2019-03-10 10:42:03",
                "Organization": 1,
            }
        ]
        payload = json.dumps(user_list)

    except Exception as e:
        # TODO: Rethink what to return...dumping exceptions is scary for data leakage
        return {"statusCode": 400, "body": "400 Bad Request\n\n" + json.dumps(str(e))}
    return {"statusCode": 200, "body": payload}
