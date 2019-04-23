import requests
import json

from library.connection import Postgres
from library.database import get_histories
from library.utils import awshandler

conn = Postgres()

@awshandler
def histories(event, context):
    organization_id = event["pathParameters"]["organization_id"]
    history_list = get_histories(conn, organization_id)
    return json.dumps(history_list)
