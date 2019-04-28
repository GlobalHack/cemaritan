import requests
import json

import library.db_queries as db_queries

from library.db_connections import Postgres
from library.utils import awshandler, aws_get_path_parameter

conn = Postgres()


@awshandler
def organizations(event, context):
    organization_list = db_queries.get_organizations(conn)
    return json.dumps([org.to_dict() for org in organization_list])


@awshandler
def get_organization(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    organization = db_queries.get_organization(connection=conn, organization_id=organization_id)
    return json.dumps(organization.to_dict())
