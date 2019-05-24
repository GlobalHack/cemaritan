
import library.db_queries as db_queries

from library.exceptions import DatabaseReturnedNone
from library.db_connections import Postgres, get_conn
from library.utils import awshandler, aws_get_path_parameter

conn = Postgres()

@awshandler
def users(event, context):
    organization_id = event["pathParameters"]["organization_id"]
    user_list = db_queries.get_users(conn, organization_id)
    return [user.to_dict() for user in user_list]

@awshandler
def get_user(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    user_id = aws_get_path_parameter(event, "user_id")
    user = db_queries.get_user(connection=conn, organization_id=organization_id, user_id=user_id)
    if user is None:
        raise DatabaseReturnedNone(f"Check object id: {user_id}")
    return user.to_dict()