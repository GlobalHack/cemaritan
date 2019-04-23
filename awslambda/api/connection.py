import requests
import json

from library.connection import Postgres
from library.database import get_connections

conn = Postgres()


def connections(event, context):
    try:
        organization_id = event["body"]["pathParameters"]["organization_id"]
        connection_list = get_connections(conn, organization_id)
        payload = json.dumps(connection_list)

    except Exception as e:
        # TODO: Rethink what to return...dumping exceptions is scary for data leakage
        return {"statusCode": 400, "body": "400 Bad Request\n\n" + json.dumps(str(e))}
    return {"statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"}, 
            "body": payload}
