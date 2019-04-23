import requests
import json

from library.connection import Postgres
from library.database import get_histories

conn = Postgres()


def histories(event, context):
    try:
        organization_id = event["body"]["pathParameters"]["organization_id"]
        history_list = get_histories(conn, organization_id)
        payload = json.dumps(history_list)

    except Exception as e:
        # TODO: Rethink what to return...dumping exceptions is scary for data leakage
        return {"statusCode": 400, "body": "400 Bad Request\n\n" + json.dumps(str(e))}
    return {"statusCode": 200, "body": payload}
