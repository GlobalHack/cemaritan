import library.db_queries as db_queries

from library.exceptions import DatabaseReturnedNone
from library.db_connections import Postgres, get_conn
from library.utils import awshandler, aws_get_path_parameter

conn = Postgres()


@awshandler
def organizations(event, context):
    organization_list = db_queries.get_organizations(conn)
    return [org.to_dict() for org in organization_list]


@awshandler
def get_organization(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    organization = db_queries.get_organization(connection=conn, organization_id=organization_id)
    if organization is None:
        raise DatabaseReturnedNone(f"Check object id: {organization_id}")
    return organization.to_dict()
