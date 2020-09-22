
# from __future__ import absolute_import
print('calling ' + __name__)

import os
import json
import io 
import zipfile 
import datetime

from typing import Dict

import boto3
import pandas as pd

import library.db_queries as db_queries
# import salesforce_api as sf

from library.utils import awshandler
from library.db_connections import Postgres
from library.models import Download

from conversion.oli_mapping import oli_mapping
from conversion.convert_hmis_to_sf import convert_files
import conversion.conversion as conv
# from conversion.salesforce_api import post_new_clients, get_recent_records
import conversion.salesforce_api as sf
import conversion.utils as utils

import another

conn = Postgres()

UPLOADS_BUCKET_NAME = 'cemaritan-dev-uploads'
DOWNLOADS_BUCKET_NAME = 'cemaritan-dev-downloads'



# OLI_MAPPING_PATH = 'oli_mapping.json'

# @awshandler
# def get_transfers_for_org(event, context):
#     # body = json.loads(event['body'])
#     # organization_id = body['organization_id']
#     # transfers = get_transfers(conn, organization_id)
#     transfers = get_transfers(conn, 1)
#     lambda_client = boto3.client('lambda')
#     for t in transfers:
#         msg = {"transfer": t.to_dict()}
#         lambda_client.invoke(FunctionName='aws-cemaritan-dataexchange-dev-do_transfer',
#                                 InvocationType='Event',
#                                 Payload=json.dumps(msg))
#     return {"Number of transfers": len(transfers)}



# Copied this function from the api.utils.py
def format_dt(dt):
    return dt.strftime('%Y/%m/%d')


# Copied this function from the api.utils.py
def get_now_datetime_formatted():
    return format_dt(datetime.datetime.now())


def parse_key_from_location(location: str) -> str:
    """Parse the key for the upload S3 object from the location parameter."""
    # https://cemaritan-dev-uploads.s3.amazonaws.com/1/20190827/Clean_CSV_Export.zip
    return location.partition('.s3.amazonaws.com')[2].strip('/')


def get_destination(upload_dict: Dict) -> str:
    """Determine if destination is 'DOWNLOAD or 'SF'"""
    if upload_dict['destination_uid'] == 6:
        return "DOWNLOAD"
    elif upload_dict['destination_uid'] == 1:
        return "SF"
    else:
        raise ValueError(f"Invalid destination_uid {upload_dict['destination_uid']} for upload.")


def unzip_s3_obj_to_dict(s3_obj, decode='utf-8') -> Dict[str, str]:
    """Unzip the body of an S3 object into a dict of filenmae -> contents."""
    filename_to_contents = {}
    with io.BytesIO(s3_obj.get('Body').read()) as tf:
        # rewind the file
        tf.seek(0)

        # Read the file as a zipfile and process the members
        with zipfile.ZipFile(tf, mode='r') as zipf:
            for subfile in [fn for fn in zipf.namelist() if not fn.startswith('__MAC')]:
                with zipf.open(subfile) as f:
                    if decode:
                        filename_to_contents[subfile] = f.read().decode(decode)
                    else:
                        filename_to_contents[subfile] = f.read()
    return filename_to_contents


def zip_json(folder, filename, data):
    """Return bytesio object containing zipped json."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode='w') as zf:
        zf.writestr(f'{folder}/{filename}', json.dumps(data))
    buffer.seek(0)
    return buffer


def zip_csvs(folder, filename, files=Dict[str, str]):
    """Return bytesio object containing zipped json."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode='w') as zf:
        for filename, data in files.items():
            zf.writestr(f'{folder}/{filename}', json.dumps(data))
    buffer.seek(0)
    return buffer

    
def put_file_in_s3(data, bucket, key):
    """Put a file in s3."""
    s3_client = boto3.client('s3')
    s3_client.put_object(ACL='private', Body=data, Bucket=bucket, Key=key)


def do_upload(event, context):
    # event = json.loads(event)
    org_id = event['organization_id']
    obj_id = event['uid']
    
    # Get upload info from db
    upload_dict = db_queries.get_upload(connection=conn, organization_id=org_id, upload_uid=obj_id).to_dict()
    
    # upload_key = upload_dict['location'].partition(UPLOADS_BUCKET_NAME)[2].strip('/')
    upload_key = parse_key_from_location(upload_dict['location'])

    # Load file from S3
    s3_client = boto3.client('s3')
    s3_obj = s3_client.get_object(Bucket=UPLOADS_BUCKET_NAME, Key=upload_key)

    # Unzip the zipfile in memory and strip down to filenames
    filename_to_contents = unzip_s3_obj_to_dict(s3_obj)
    filename_to_contents = {k.split('/')[1]:v for k,v in filename_to_contents.items()}

    # Convert to SF
    res = convert_files(filename_to_contents, oli_mapping)
    # print(res)

    destination = get_destination(upload_dict)
    if destination == "SF":

        # if sf
        # Push to SF
        client_objs = [obj['OLI_Client__c'] for obj in res.values()]
        # TO REMOVE
        # TEMPORARILY limit the number of clients added to SF
        client_objs = client_objs[:5]
        ids = sf.post_new_clients(client_objs)

    elif destination == "DOWNLOAD":
        # if download
        download_key = f'{org_id}/{get_now_datetime_formatted()}/salesforce.zip'
        zipped = zip_json('salesforce', 'salesforce.json', res)
        # put in S3
        put_file_in_s3(zipped, DOWNLOADS_BUCKET_NAME, download_key)
        db_queries.create_download(connection=conn,
                                    organization_id=org_id,
                                    download=Download({'name': 'Upload',
                                        'transfer_name':'Upload',
                                        'history_uid': 1,
                                        'bucket_name': DOWNLOADS_BUCKET_NAME,
                                        'obj_name': download_key
                                    }))




def do_transfer(event, context):
    org_id = event['organization_id']
    obj_id = event['uid']

    transfer_dict = db_queries.get_transfer(connection=conn, organization_id=org_id, transfer_id=obj_id).to_dict()

    # Logic to determine source and destination
    # Eventually, the flow should be like this:
    # 1. Get source type and connector
    # 2. Get destination type and connector
    # 3. If both source and destination are valid, proceed.
    # 4. Get data from source and transform to HUD.
    # 5. Transform data to destination and push to destination.
    if transfer_dict['source'] == 'SF' and transfer_dict['destination'] == 'Secure Download':
        # Get data from SF
        updated_objects = sf.get_recent_records(minutes=360)
        if len(updated_objects) > 0:
            print(f"{len(updated_objects)} updates found.")
            # Pass individual objects to single convert endpoint.
            converted_objects = conv.convert_many(updated_objects)
            converted_csvs = {filename: utils.write_csvfile_to_str(csv) for filename, csv in converted_objects.items()}
            # save_files_to_s3(bucket=S3_BUCKET_NAME, csv_files=consolidated_csv_files, prefix=prefix)
            download_key = f'{org_id}/{get_now_datetime_formatted()}/salesforce.zip'
            zipped = zip_csvs('salesforce', 'HUD', converted_csvs)
            # put in S3
            put_file_in_s3(zipped, DOWNLOADS_BUCKET_NAME, download_key)
            db_queries.create_download(connection=conn,
                                        organization_id=org_id,
                                        download=Download({'name': transfer_dict['name'],
                                            'transfer_name': transfer_dict['name'],
                                            'history_uid': 1,
                                            'bucket_name': DOWNLOADS_BUCKET_NAME,
                                            'obj_name': download_key
                                        }))
    else:
        # No other kinds are implemented yet.
        pass





############################# Connectors ############################# 


### Connections ###

# class Connection:

#     def __init__(self, mapping):
#         self.mapping = mapping

#     def get_data(self):
#         raise NotImplementedError()

#     def convert(self):
#         raise NotImplementedError()

#     def send_data(self):
#         raise NotImplementedError()
    

# class Upload(Connection):
#     """Can be a source, but not a destination.
#     """
#     def __init__(self, mapping, location: str):
#         super().__init__(self, mapping=mapping)
#         self.location = location
    
#     def get_data(self):
#         s3_client = boto3.client('s3')


# class Download(Connection):
#     """Can be a destination, but not a source.
#     """
#     def __init__(self, mapping, location: str):
#         super().__init__(self, mapping=mapping)
#         self.location = location

#     def get_data(self):
#         pass

#     def convert(self):
#         if mapping is not None:
#             # Convert
#             pass

#     def put_data(self):
#         s3_client = boto3.client('s3')
#         s3.Object('cemaritan-dev-test', f'test_{rand_int}.txt').put(Body='test body')


# class Salesforce(Connection):
#     """Can be both a source and a destination.
#     """
#     def __init__(self, mapping):
#         super().__init__(self, mapping=mapping)
        