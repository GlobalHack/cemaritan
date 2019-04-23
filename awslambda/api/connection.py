import requests
import json

from library.connection import Postgres
from library.database import get_connections
from library.utils import awshandler

conn = Postgres()

@awshandler
def connections(event, context):
    organization_id = event["pathParameters"]["organization_id"]
    connection_list = get_connections(conn, organization_id)
    return json.dumps(connection_list)

