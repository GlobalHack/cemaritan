import requests
import json

# from library.connection import Postgres
# from library.database import *

# define DB connection here


def organizations(event, context):
    try:
        s = event["body"]

        # replace organization_list here with actual database function call
        organization_list = [
            {"UID": 1, "Name": "OLI", "CreatedDate": "2019-03-13 20:42:03"},
            {"UID": 2, "Name": "SPC", "CreatedDate": "2019-03-15 01:03:03"},
            {"UID": 3, "Name": "OLI 2", "CreatedDate": "2019-03-18 20:42:03"},
            {"UID": 4, "Name": "neworg", "CreatedDate": "2019-03-18T12:34:56"},
            {"UID": 5, "Name": "neworg", "CreatedDate": "2019-03-18T12:34:56"},
            {"UID": 6, "Name": "neworg", "CreatedDate": "2019-03-18T12:34:56"},
            {"UID": 7, "Name": "neworg", "CreatedDate": "2019-03-18T12:34:56"},
            {"UID": 8, "Name": "neworg", "CreatedDate": "2019-03-18T12:34:56"},
            {"UID": 9, "Name": "neworg", "CreatedDate": "2019-03-18T12:34:56"},
        ]
        payload = json.dumps(organization_list)

    except Exception as e:
        # TODO: Rethink what to return...dumping exceptions is scary for data leakage
        return {"statusCode": 400, "body": "400 Bad Request\n\n" + json.dumps(str(e))}
    return {"statusCode": 200, "body": payload}
