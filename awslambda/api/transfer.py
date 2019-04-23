import requests
import json

from library.db_connections import Postgres
from library.db_queries import get_transfers
from library.utils import awshandler

conn = Postgres()

@awshandler
def transfers(event, context):
    organization_id = event["pathParameters"]["organization_id"]
    transfer_list = get_transfers(conn, organization_id)
    return json.dumps([trans.to_dict() for trans in transfer_list])


@awshandler
def create_transfers(event, context):
    return json.dumps("Data not saved yet.")
