import requests
import json

import library.db_queries as db_queries

from library.db_connections import Postgres
from library.utils import awshandler, aws_get_path_parameter

conn = Postgres()

@awshandler
def connections(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    connection_list = db_queries.get_connections(conn, organization_id)
    return json.dumps([connection.to_dict() for connection in connection_list])


@awshandler
def get_connection(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    connection_id = aws_get_path_parameter(event, "connection_id")
    connection = db_queries.get_connection(connection=conn, organization_id=organization_id, connection_id=connection_id)
    return json.dumps(connection.to_dict())