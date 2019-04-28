import requests
import json

import library.db_queries as db_queries

from library.db_connections import Postgres
from library.utils import awshandler, aws_get_path_parameter

conn = Postgres()

@awshandler
def transfers(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    transfer_list = db_queries.get_transfers(conn, organization_id)
    return json.dumps([trans.to_dict() for trans in transfer_list])


@awshandler
def create_transfer(event, context):
    return json.dumps("Data not saved yet.")


@awshandler
def get_transfer(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    transfer_id = aws_get_path_parameter(event, "transfer_id")
    transfer = db_queries.get_transfer(connection=conn, organization_id=organization_id, transfer_id=transfer_id)
    return json.dumps(transfer.to_dict())