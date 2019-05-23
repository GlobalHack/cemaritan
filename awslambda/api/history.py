import requests
import json

import library.db_queries as db_queries
from models import History

from library.exceptions import DatabaseReturnedNone
from library.db_connections import Postgres, get_conn
from library.utils import awshandler, aws_get_path_parameter

conn = Postgres()


@awshandler
def histories(event, context):
    organization_id = event["pathParameters"]["organization_id"]
    history_list = db_queries.get_histories(conn, organization_id)
    return [hist.to_dict() for hist in history_list]


@awshandler
def get_history(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    history_id = aws_get_path_parameter(event, "history_id")
    history = db_queries.get_history(
        connection=conn, organization_id=organization_id, history_id=history_id
    )
    if history is None:
        raise DatabaseReturnedNone(f"Check object id: {history_id}")
    return history.to_dict()


@awshandler
def create_history(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    body = json.loads(event["body"])
    history_obj = History(body)
    response = db_queries.create_history(connection=conn, history=history_obj)
    tup = response[0][0]
    return {tup[0]: tup[1]}
