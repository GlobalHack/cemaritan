"""
This module exposes the conversion functionality as an API and 
is ready to be deployed an AWS Lambda function.

The boto3 python library for working with AWS is available in AWS Lambda
environments without importing them, but it is imported here for local testing.

ENVIRONMENTAL VARIABLES:
s3_bucket' containing the name of the S3 bucket that the csv files should be saved in.

"""

import os
import json
from typing import Dict

import boto3

from conversion import convert, write_records_to_str

# Get S3 bucket name from Env Var.
S3_BUCKET_NAME = os.getenv('s3_bucket', 'cemaritan-dev-test')


def save_string_to_s3(s3, bucket: str, name: str, content: str):
    """Save `content` as a file named `name` in bucket `bucket`.
    
    Parameters
    ----------
    s3 : boto3.resource
        A boto3 S3 resource object.
    bucket : str
        Name of the bucket.
    name : str
        Filename to save string as.
    content : str
        Content of the file.
    """
    s3.Object(bucket, name).put(Body=content)


def save_files_to_s3(bucket: str, files: Dict[str, Dict[str, str]]):
    """Save content of HMIS files to S3."""
    # Get S3 resource object
    s3 = boto3.resource('s3')
    # Save each csv HMIS file to S3.
    for filename, fields in files.items():
        save_string_to_s3(s3=s3, bucket=bucket, name=filename, content=write_records_to_str(fields))



### Lambda handler

def endpoint(event, context):
    # Get POST body which should be a json object containing high level Salesforce objects.
    converted_data = convert(json.loads(event['body']))
    
    # Save results to S3
    save_files_to_s3(bucket=S3_BUCKET_NAME, files=converted_data)

    # Return results for testing.
    # Eventually remove this and return a status message.
    response = {
        "statusCode": 200,
        "body": json.dumps(converted_data)
    }
    return response