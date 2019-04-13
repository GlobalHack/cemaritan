import requests
import json

# from library.connection import Postgres
# from library.database import *

# define DB connection here


def transfers(event, context):
    try:
        s = event["body"]

        # replace transfer_list here with actual database function call
        transfer_list = [
            {
                "UID": 1,
                "Name": "CW to SF",
                "CreatedDate": "2019-03-20 20:42:03",
                "CreatedBy": 1,
                "Organization": 1,
                "Source": 2,
                "SourceMapping": 2,
                "Destination": 1,
                "DestinationMapping": 1,
                "StartDateTime": "2019-03-13 20:42:03",
                "Frequency": "1 day",
                "RecordFilter": "filter a",
                "Active": 1,
            },
            {
                "UID": 2,
                "Name": "SF to CW",
                "CreatedDate": "2019-03-13 20:42:03",
                "CreatedBy": 1,
                "Organization": 1,
                "Source": 1,
                "SourceMapping": 1,
                "Destination": 2,
                "DestinationMapping": 2,
                "StartDateTime": "2019-03-13 20:42:03",
                "Frequency": "1 hour",
                "RecordFilter": "filter b",
                "Active": 0,
            },
        ]
        payload = json.dumps(transfer_list)

    except Exception as e:
        # TODO: Rethink what to return...dumping exceptions is scary for data leakage
        return {"statusCode": 400, "body": "400 Bad Request\n\n" + json.dumps(str(e))}
    return {"statusCode": 200, "body": payload}



def create_transfers(event, context):
    try:
        s = event["body"]
        # Ignore data for now.

        payload = json.dumps('Data not saved yet.')

    except Exception as e:
        # TODO: Rethink what to return...dumping exceptions is scary for data leakage
        return {"statusCode": 400, "body": "400 Bad Request\n\n" + json.dumps(str(e))}
    return {"statusCode": 200, "body": payload}