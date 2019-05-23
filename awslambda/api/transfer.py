import requests
import json

import library.db_queries as db_queries

from models import History
from library.exceptions import DatabaseReturnedNone
from library.db_connections import Postgres, get_conn
from library.utils import awshandler, aws_get_path_parameter, aws_get_json_body


from models import Transfer

conn = Postgres()


@awshandler
def transfers(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    transfer_list = db_queries.get_transfers(conn, organization_id)
    return [trans.to_dict() for trans in transfer_list]


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


@awshandler
def create_transfer(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    body = json.loads(event["body"])
    transfer_obj = Transfer(body)
    response = db_queries.create_transfer(connection=conn, transfer=transfer_obj)
    tup = response[0][0]

    # parse transfer content
    uid = transfer_obj._uid
    name = transfer_obj._name
    created_date = transfer_obj._created_date
    created_by = transfer_obj._created_by
    organization_id = transfer_obj._organization
    source = transfer_obj._source
    source_mapping = transfer_obj._source_mapping
    destination = transfer_obj._destination
    destination_mapping = transfer_obj._destination_mapping
    start_datetime = transfer_obj._start_datetime
    frequency = transfer_obj._frequency
    record_filter = transfer_obj._record_filter
    active = transfer_obj._active
    history_dict = {
        "type": "Transfer",
        "action": "Transfer Action",  # TODO: temporary, maybe change?
        "date": created_date,
        "name": name,
        "details": "Some Details",
        "source_uid": uid,
        "organization": organization_id,
    }
    history_obj = History(history_dict)
    db_queries.create_history(conn, history_obj)
    # TODO: Replace the above with a boto3 call

    return {tup[0]: tup[1]}


def delete_transfer(transfer_id):
    """Temporary function for testing. Eventually this 
    will be built out into a full handler."""
    db_queries.delete_transfer(conn, transfer_id)
