import requests
import json

import library.db_queries as db_queries

from library.db_connections import Postgres
from library.utils import awshandler, aws_get_path_parameter

conn = Postgres()

@awshandler
def mappings(event, context):
    organization_id = event["pathParameters"]["organization_id"]
    mapping_list = db_queries.get_mappings(conn, organization_id)
    return json.dumps([mapping.to_dict() for mapping in mapping_list])


@awshandler
def get_mapping(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    mapping_id = aws_get_path_parameter(event, "mapping_id")
    mapping = db_queries.get_mapping(connection=conn, organization_id=organization_id, mapping_id=mapping_id)
    return json.dumps(mapping.to_dict())