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


@awshandler
def get_download_link(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    download_id = aws_get_path_parameter(event, "download_id")
    download = db_queries.get_download(
        connection=conn, organization_id=organization_id, download_id=download_id
    )
    file_location_info = download._file_location_info
    if file_location_info is not None:
        link = _generate_download_link(file_locatinon_info)
    else:
        link = 'No link created'
    return json.dumps({'download_link': link})


def _generate_download_link(file_locatinon_info: str) -> str:
    return f'fake_link_for_{file_locatinon_info}'