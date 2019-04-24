import requests
import json

from library.db_connections import Postgres
from library.db_queries import get_mappings
from library.utils import awshandler

conn = Postgres()

@awshandler
def mappings(event, context):
    organization_id = event["pathParameters"]["organization_id"]
    mapping_list = get_mappings(conn, organization_id)
    return json.dumps([mapping.to_dict() for mapping in mapping_list])
