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
import datetime

from utils import *
from conversion import convert

# Get S3 bucket name from Env Var.
S3_BUCKET_NAME = os.getenv('s3_bucket', 'cemaritan-dev-test')


### Lambda handlers

def convertsingle(event, context):
    """
    Accept a single JSON object which should be an SF record, convert it to HMIS 
    format, and output.
    """
    print(context)
    # Get POST body which should be a json object containing high level Salesforce objects.
    single_record = json.loads(event['body'])
    
    # Convert record
    converted_data = convert(single_record)

    # Save results to S3
    prefix = str(datetime.datetime.now()).replace(' ', 'T')
    save_files_to_s3(bucket=S3_BUCKET_NAME, csv_files=converted_data, prefix=prefix)

    # Return results for testing.
    # Eventually remove this and return a status message.
    response = {
        "statusCode": 200,
        "body": json.dumps(converted_data)
    }
    return response


def convertbulk(event, context):
    """Accept a JSON array of SF records, convert to HMIS format, and output.
    
    Output options are limited to saving to S3 right now.
    """
    # Get payload from request. Should load as a list of SF objects. List[SfRecord]
    list_of_sf_objects = json.loads(event['body'])
    # Convert all objects to HMIS format.
    list_of_converted_objects = [convert(obj) for obj in list_of_sf_objects]
    # Consolidate into a single set of csv files.
    consolidated_csv_files = combine_csv_files(csv_files=list_of_converted_objects)
    # Pass the converted objects to be combined, written to strings, and saved as files in S3.
    save_files_to_s3(bucket=S3_BUCKET_NAME, csv_files=consolidated_csv_files)
    # Send back a confirmation message.
    response = {
        "statusCode": 200,
        "body": "Records converted and saved."
    }
    return response
    