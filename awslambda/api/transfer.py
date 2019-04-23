import requests
import json

from library.connection import Postgres
from library.database import get_transfers
from library.utils import awshandler

conn = Postgres()

@awshandler
def transfers(event, context):
    organization_id = event["pathParameters"]["organization_id"]
    transfer_list = get_transfers(conn, organization_id)
    return json.dumps(transfer_list)


@awshandler
def create_transfers(event, context):
    return json.dumps("Data not saved yet.")
