import requests
import json

import library.db_queries as db_queries

from library.exceptions import DatabaseReturnedNone
from library.db_connections import Postgres
from library.utils import awshandler, aws_get_path_parameter

conn = Postgres()


@awshandler
def downloads(event, context):
    organization_id = event["pathParameters"]["organization_id"]
    download_list = db_queries.get_downloads(conn, organization_id)
    return [dl.to_dict() for dl in download_list]


@awshandler
def get_download(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    download_id = aws_get_path_parameter(event, "download_id")
    download = db_queries.get_download(
        connection=conn, organization_id=organization_id, download_id=download_id
    )
    if download is None:
        raise DatabaseReturnedNone(f"Check object id: {download_id}")
    return download.to_dict()
