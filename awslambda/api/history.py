import requests
import json

from library.db_connections import Postgres
from library.db_queries import get_histories
from library.utils import awshandler

conn = Postgres()

@awshandler
def histories(event, context):
    organization_id = event["pathParameters"]["organization_id"]
    history_list = get_histories(conn, organization_id)
    return json.dumps([hist.to_dict() for hist in history_list])
