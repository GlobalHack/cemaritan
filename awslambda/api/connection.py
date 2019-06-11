import library.db_queries as db_queries

from library.exceptions import DatabaseReturnedNone
from library.db_connections import Postgres, get_conn
from library.utils import awshandler, aws_get_path_parameter, de_handler

conn = Postgres()

@awshandler
def connections(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    connection_list = db_queries.get_connections(conn, organization_id)
    return [connection.to_dict() for connection in connection_list]


@awshandler
def get_connection(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    connection_id = aws_get_path_parameter(event, "connection_id")
    connection = db_queries.get_connection(connection=conn, organization_id=organization_id, connection_id=connection_id)
    if connection is None:
        raise DatabaseReturnedNone(f"Check object id: {connection_id}")
    return connection.to_dict()
