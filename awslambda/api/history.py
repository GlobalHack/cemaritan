import requests
import json

import library.db_queries as db_queries

from library.db_connections import Postgres
from library.utils import awshandler, aws_get_path_parameter

conn = Postgres()

@awshandler
def histories(event, context):
    organization_id = event["pathParameters"]["organization_id"]
    history_list = db_queries.get_histories(conn, organization_id)
    return json.dumps([hist.to_dict() for hist in history_list])


@awshandler
def get_history(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    history_id = aws_get_path_parameter(event, "history_id")
    print(f'history id {history_id}')
    history = db_queries.get_history(connection=conn, organization_id=organization_id, history_id=history_id)
    print(history)
    if history is None:
        return {"thing": "None"}
    return json.dumps(history.to_dict())