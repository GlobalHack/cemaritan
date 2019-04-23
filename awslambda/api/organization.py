import requests
import json

from library.db_connections import Postgres
from library.db_queries import get_organizations
from library.utils import awshandler

conn = Postgres()


@awshandler
def organizations(event, context):
    organization_list = get_organizations(conn)
    return json.dumps([org.to_dict() for org in organization_list])

