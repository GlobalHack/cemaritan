import requests
import json

from library.connection import Postgres
from library.database import get_transfers

conn = Postgres()


def transfers(event, context):
    try:
        organization_id = event["body"]["pathParameters"]["organization_id"]
        transfer_list = get_transfers(conn, organization_id)
        payload = json.dumps(transfer_list)

    except Exception as e:
        # TODO: Rethink what to return...dumping exceptions is scary for data leakage
        return {"statusCode": 400, "body": "400 Bad Request\n\n" + json.dumps(str(e))}
    return {"statusCode": 200, "body": payload}


def create_transfers(event, context):
    try:
        s = event["body"]
        # Ignore data for now.

        payload = json.dumps("Data not saved yet.")

    except Exception as e:
        # TODO: Rethink what to return...dumping exceptions is scary for data leakage
        return {"statusCode": 400, "body": "400 Bad Request\n\n" + json.dumps(str(e))}
    return {"statusCode": 200, "body": payload}
