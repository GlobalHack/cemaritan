import requests
import json

# from library.connection import Postgres
# from library.database import *

# define DB connection here


def histories(event, context):
    try:
        s = event["body"]

        # replace history_list here with actual database function call
        history_list = [
            {
                "Type": "sampleType",
                "Action": "sampleAction",
                "Date": "2019-03-10 12:34:56",
                "CreatedByUser": 1,
                "Name": "Joe Dirt",
                "UID": 1,
                "Details": "someDetails",
                "SourceUID": 1,
                "Organization": 1,
            }
        ]
        payload = json.dumps(history_list)

    except Exception as e:
        # TODO: Rethink what to return...dumping exceptions is scary for data leakage
        return {"statusCode": 400, "body": "400 Bad Request\n\n" + json.dumps(str(e))}
    return {"statusCode": 200, "body": payload}
