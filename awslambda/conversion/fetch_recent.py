"""
Contains Lambda function to retrieve recently updated SF objects and
send them to the conversion endpoints.
"""

import os

import requests

import salesforce_api
import utils

single_convert_url = 'https://adtzjz51x8.execute-api.us-east-1.amazonaws.com/dev/convertsingle'
bulk_convert_url = 'https://adtzjz51x8.execute-api.us-east-1.amazonaws.com/dev/convertbulk'

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

    # Send email to user.
    try:
        if len(updated_objects) > 0:
            server = 'email-smtp.us-east-1.amazonaws.com', 587
            un = os.getenv('ses_username')
            pw = os.getenv('ses_password')

            msg = f"{len(updated_objects)} updates found."
            utils.send_mail(msg=msg, 
                to_add=['cemaritanproject@gmail.com',], 
                from_add='mattscomp21@gmail.com',
                smts_server=server,
                login=(un, pw),
                subject='Cemaritan: records updated'
                )
    except Exception as e:
        print(e)



