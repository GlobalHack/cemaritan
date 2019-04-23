import requests
import json

from library.connection import Postgres
from library.database import get_organizations

conn = Postgres()


def organizations(event, context):
    try:
        organization_list = get_organizations(conn)
        payload = json.dumps(organization_list)

    except Exception as e:
        # TODO: Rethink what to return...dumping exceptions is scary for data leakage
        return {"statusCode": 400, "body": "400 Bad Request\n\n" + json.dumps(str(e))}
    return {"statusCode": 200, "body": payload}
