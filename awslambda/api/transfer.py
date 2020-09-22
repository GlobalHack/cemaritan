import json

import library.db_queries as db_queries

from library.exceptions import DatabaseReturnedNone
from library.db_connections import Postgres, get_conn
from library.utils import awshandler, aws_get_path_parameter, get_now_datetime_formatted

from library.models import Transfer, History

import boto3 

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
    transfer = db_queries.get_transfer(connection=conn, organization_id=organization_id, transfer_id=transfer_id)
    if transfer is None:
        raise DatabaseReturnedNone(f"Check object id: {transfer_id}")
    return transfer.to_dict()


@awshandler
def create_transfer(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    body = json.loads(event['body'])
    transfer_obj = Transfer(body)
    response = db_queries.create_transfer(connection=conn, organization_id=organization_id, transfer=transfer_obj)
    tup = response[0][0]
    transfer_dict = transfer_obj.to_dict()
    db_queries.create_history(connection=conn,
                                organization_id=organization_id,
                                history=History({'type': 'Transfer',
                                'action': 'Created',
                                'datetime': get_now_datetime_formatted(),
                                'name': transfer_dict['name'],
                                'details': '',
                                'source_uid': transfer_dict['source_uid'],
                                'organization': organization_id
                                }))
    # Run transfer immediately
    call_do_transfer(organization_id, tup[1])
    return {tup[0]: tup[1]}


@awshandler
def update_transfer(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    transfer_id = aws_get_path_parameter(event, "transfer_id")
    body = json.loads(event['body']) 
    transfer_obj = Transfer(body)
    result = db_queries.update_transfer(connection=conn, organization_id=organization_id, transfer_id=transfer_id, transfer=transfer_obj)
    return {'message': 'success'}


def delete_transfer(transfer_id):
    """Temporary function for testing. Eventually this 
    will be built out into a full handler."""
    db_queries.delete_transfer(conn, transfer_id)


def call_do_transfer(org_id: str, uid: str):
    """Call the `do_upload` function with the uid of an upload record."""
    # print(uid)
    msg = {"organization_id" : org_id, "uid": uid}
    lambda_client = boto3.client('lambda')
    lambda_client.invoke(FunctionName='aws-cemaritan-dataexchange-dev-do_transfer',
                            InvocationType='Event',
                            Payload=json.dumps(msg))


@awshandler
def get_frequencies_list(event, context):
    """Return list of acceptable frequencies."""
    results = db_queries.get_frequencies_list(conn)
    return [fr.to_dict() for fr in results]