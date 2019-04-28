import requests
import json

from library.db_connections import Postgres
from library.db_queries import get_histories
from library.utils import awshandler

conn = Postgres()

@awshandler
def histories(event, context):
    organization_id = event["pathParameters"]["organization_id"]
    history_list = get_histories(conn, organization_id)
    return json.dumps([hist.to_dict() for hist in history_list])


@awshandler
def get_history(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    history_id = aws_get_path_parameter(event, "history_id")
    return json.dumps({'org':organization_id, 'history':history_id})
    history = db_queries.get_history(organization_id=organization_id, history_id=history_id)
    return json.dumps(history.to_dict())