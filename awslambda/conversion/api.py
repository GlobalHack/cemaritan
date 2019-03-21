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

import salesforce_api
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

    # Send success notifcation.
    #send_notification(n=1)

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
    prefix = str(datetime.datetime.now()).replace(' ', 'T')
    save_files_to_s3(bucket=S3_BUCKET_NAME, csv_files=consolidated_csv_files, prefix=prefix)
    # Send success notification.
    #send_notification(len(list_of_converted_objects))
    # Send back a confirmation message.
    response = {
        "statusCode": 200,
        "body": "Records converted and saved."
    }
    return response
    

def file_upload(event, context):
    """Accept a file with either a single or an array of Salesforce objects and convert them."""
    s = event['body']
    s_split = s.split('\n')
    payload = '\n'.join(s_split[3:-2])
    try:
        obj = json.loads(payload)
        if isinstance(obj, list):
            obj_len = len(obj)
            list_of_converted_objects = [convert(obj) for obj in obj]
            # Consolidate into a single set of csv files.
            consolidated_csv_files = combine_csv_files(csv_files=list_of_converted_objects)
            # Pass the converted objects to be combined, written to strings, and saved as files in S3.
            prefix = str(datetime.datetime.now()).replace(' ', 'T')
            save_files_to_s3(bucket=S3_BUCKET_NAME, csv_files=consolidated_csv_files, prefix=prefix)
        else:
            obj_len = 1
            # Convert record
            converted_data = convert(obj)

            # Save results to S3
            prefix = str(datetime.datetime.now()).replace(' ', 'T')
            save_files_to_s3(bucket=S3_BUCKET_NAME, csv_files=converted_data, prefix=prefix)

        # Send success notification.
        send_notification(n=obj_len)
    except Exception as e:
        return {
            'statusCode': 400,
            'body': '400 Bad Request\n\n' + json.dumps(str(e))
            }
    
    return {
        'statusCode': 200,
        'body': 'Upload successful.'
    }


def send_notification(n):
    # Send email to user.
    try:
        server = 'email-smtp.us-east-1.amazonaws.com', 587
        un = os.getenv('ses_username')
        pw = os.getenv('ses_password')

        msg = f"{n} updates saved to cloud storage."
        send_mail(msg=msg, 
            to_add=['cemaritanproject@gmail.com'], 
            from_add='mattscomp21@gmail.com',
            smts_server=server,
            login=(un, pw),
            subject='Cemaritan: records updated'
            )
    except Exception as e:
        print(e)


def post_new_client(event, context):
    """Post a new client record."""
    data = extact_form_data(event)
    first_name = data['firstname']
    last_name = data['lastname']
    # Load credentials from local file. If no filename is passed, will try to load from environmental variables.
    creds = salesforce_api.get_credentials()
    # Create authentication header by requesting bearer token.
    headers = salesforce_api.get_auth_header(**creds)
    id_ = salesforce_api.post_new_client(first_name=first_name, last_name=last_name, headers=headers)
    print(id_)
    return {
        'statusCode': 200,
        'body': f'Record was synced with SalesForce. Id: {id_}'
    }