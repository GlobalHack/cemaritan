import requests
import json

import library.db_queries as db_queries

from library.exceptions import DatabaseReturnedNone
from library.db_connections import Postgres
from library.utils import awshandler, aws_get_path_parameter, aws_get_json_body

conn = Postgres()


@awshandler
def transfers(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    transfer_list = db_queries.get_transfers(conn, organization_id)
    return [trans.to_dict() for trans in transfer_list]


@awshandler
def create_transfer(event, context):
    # parse transfer content
    body = aws_get_json_body(event)
    user_id = body["user_id"]
    name = body["name"]
    created_date = body["created_date"]
    created_by = body["created_by"]
    organization_id = body["organization_id"]
    source = body["source"]
    source_mapping = body["source_mapping"]
    destination = body["destination"]
    destination_mapping = body["destination_mapping"]
    start_date_time = body["start_date_time"]
    frequency = body["frequency"]
    record_filter = body["record_filter"]
    active = body["active"]
    # create transfer object
    db_queries.create_transfer(
        connection=conn,
        user_id=user_id,
        name=name,
        created_date=created_date,
        created_by=created_by,
        organization_id=organization_id,
        source=source,
        source_mapping=source_mapping,
        destination=destination,
        destination_mapping=destination_mapping,
        start_date_time=start_date_time,
        frequency=frequency,
        record_filter=record_filter,
        active=active,
    )
    # create corresponding history object
    db_queries.create_history()
    return "Data not saved yet."


@awshandler
def get_transfer(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    transfer_id = aws_get_path_parameter(event, "transfer_id")
    transfer = db_queries.get_transfer(
        connection=conn, organization_id=organization_id, transfer_id=transfer_id
    )
    if transfer is None:
        raise DatabaseReturnedNone(f"Check object id: {transfer_id}")
    return transfer.to_dict()
