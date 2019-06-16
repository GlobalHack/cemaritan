from datetime import datetime

import library.db_queries as db_queries

from library.exceptions import DatabaseReturnedNone
from library.db_connections import Postgres, get_conn
from library.utils import awshandler, aws_get_path_parameter

from models.Models import Upload

import boto3 

conn = Postgres()

UPLOAD_LINK_EXPIRATION = 120

UPLOAD_BUCKET_NAME = 'cemaritan-dev-uploads'

@awshandler
def get_upload_link(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    # body = json.loads(event['body'])
    # The better way to do this might be to send back a signed URL 
    # to the client and have them upload to S3. 
    # Then have the client make another post to kick off the conversion process.
    key = '/'.join([organization_id, _get_date(), '${filename}'])
    response = _create_presigned_post(UPLOAD_BUCKET_NAME, key)
    return response


def _create_presigned_post(bucket_name, object_name,
                          fields=None, conditions=None, expiration=UPLOAD_LINK_EXPIRATION):
    """Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """

    # Generate a presigned S3 POST URL
    s3_client = boto3.client('s3')

    response = s3_client.generate_presigned_post(bucket_name,
                                                 object_name,
                                                 Fields=fields,
                                                 Conditions=conditions,
                                                 ExpiresIn=expiration)

    # The response contains the presigned URL and required fields
    return response


def _get_date():
    return datetime.today().strftime('%Y%m%d')