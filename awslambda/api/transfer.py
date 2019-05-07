import requests
import json

import library.db_queries as db_queries

from library.exceptions import DatabaseReturnedNone
from library.db_connections import Postgres
from library.utils import awshandler, aws_get_path_parameter

from models import Transfer

conn = Postgres()

@awshandler
def transfers(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    transfer_list = db_queries.get_transfers(conn, organization_id)
    return [trans.to_dict() for trans in transfer_list]


#@awshandler
def create_transfer(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    body = json.loads(event['body'])
    transfer_obj = Transfer(body)
    response = db_queries.create_transfer(connection=conn, transfer=transfer_obj)
    return {'message': 'test'}


@awshandler
def get_transfer(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    transfer_id = aws_get_path_parameter(event, "transfer_id")
    transfer = db_queries.get_transfer(connection=conn, organization_id=organization_id, transfer_id=transfer_id)
    if transfer is None:
        raise DatabaseReturnedNone(f"Check object id: {transfer_id}")
    return transfer.to_dict()