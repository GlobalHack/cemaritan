import requests
import json

from library.connection import Postgres
from library.database import get_users
from library.utils import awshandler

conn = Postgres()

@awshandler
def users(event, context):
    organization_id = event["pathParameters"]["organization_id"]
    user_list = get_users(conn, organization_id)
    return json.dumps([user.to_dict() for user in user_list])
