"""
Contains Lambda function to retrieve recently updated SF objects and
send them to the conversion endpoints.
"""

import os

import requests

import salesforce_api

single_convert_url = 'https://adtzjz51x8.execute-api.us-east-1.amazonaws.com/dev/convertsingle'


def fetch_updated_and_send_to_conversion(event, context):
    """Main function to retrieve recently updated SF objects
    and send the to the converion endpoints.
    """
    # Load credentials from local file. If no filename is passed, will try to load from environmental variables.
    creds = salesforce_api.get_credentials()
    # Create authentication header by requesting bearer token.
    headers = salesforce_api.get_auth_header(**creds)
    # Retrieve recent updates.
    updated_objects = salesforce_api.get_recent_records(headers=headers, minutes=1)
    print(f"{len(updated_objects)} updates found.")
    for obj in updated_objects:
        print(obj)
    # Pass individual objects to single convert endpoint.
    responses = []
    for obj in updated_objects:
        responses.append(requests.post(url=single_convert_url, json=obj, headers=headers))
    



