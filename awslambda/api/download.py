import boto3
from botocore.exceptions import ClientError

import library.db_queries as db_queries

from library.exceptions import DatabaseReturnedNone
from library.db_connections import Postgres
from library.utils import awshandler, aws_get_path_parameter

conn = Postgres()

DOWNLOAD_LINK_EXPIRATION = 120


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
    bucket_name = download._bucket_name
    obj_name = download._obj_name
    if bucket_name is not None:
        link = _generate_download_link(bucket_name, obj_name)
        expiration = DOWNLOAD_LINK_EXPIRATION
    else:
        link = 'No link created'
        expiration = 0
    return {'download_link': link, 'expiration': expiration}


def _generate_download_link(bucket_name: str, obj_name: str) -> str:
    return _create_presigned_url(bucket_name=bucket_name, obj_name=obj_name)


def _create_presigned_url(bucket_name, obj_name, expiration=DOWNLOAD_LINK_EXPIRATION):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': obj_name},
                                                    ExpiresIn=expiration)
    # The response contains the presigned URL
    return response