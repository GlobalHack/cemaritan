
import library.db_queries as db_queries

from library.exceptions import DatabaseReturnedNone
from library.db_connections import Postgres, get_conn
from library.utils import awshandler, aws_get_path_parameter

conn = Postgres()

# @awshandler
# def users(event, context):
#     organization_id = event["pathParameters"]["organization_id"]
#     user_list = db_queries.get_users(conn, organization_id)
#     return [user.to_dict() for user in user_list]

@awshandler
def get_user(event, context):
    # organization_id = aws_get_path_parameter(event, "organization_id")
    # user_id = aws_get_path_parameter(event, "user_id")
    # print('event')
    # print(event)
    # print('context')
    # print(context)
    firebase_id = event['requestContext']['authorizer']['principalId']
    user = db_queries.get_user_by_auth_id(connection=conn, auth_id=firebase_id, auth_service=None)
    user_dict = user.to_dict()
    user_uid = user_dict['uid']
    user = db_queries.get_user_by_uid(connection=conn, user_uid=user_uid)
    if user is None:
        raise DatabaseReturnedNone(f"Bad auth id.")
    return user.to_dict()