# coding: utf-8

""""
This module wraps interactions with the salesforce API in order to authenticate and 
retrieve entire client records.

In the future it may also support updating records.

Example:
# Load credentials from local file. If no filename is passed, will try to load from environmental variables.
creds = get_credentials(config_file='/Users/userfolder/cemaritan_salesforce_temp.txt')
# Create authentication header by requesting bearer token.
headers = get_auth_header(**creds)
# Retrieve complete client record.
record = get_complete_client_record(oli_client__c_id=record_id, headers=headers)

The compete client record schema, which the conversion code will accept, has OLI Salesforce
objects as the keys, and a single object or array of objects of that object type as the value.
{"OLI_Client__c" : _OLI_Client__c_object_,
 "Snapshots_Forms__c": [_Snapshots_Forms__c_object_1_, _Snapshots_Forms__c_object_2_]
}

"""

import os
from typing import Dict
import configparser

import requests

### Load credentials from file or environmental variables.

def get_credentials(config_file: str=None) -> Dict[str, str]:
    """Returns a dict with credentials. 
    
    If a config filename is passed, will try to read from section 'sf'.
    Else will try to read from environmental variables.
    """
    if config_file:
        cp = configparser.ConfigParser()
        cp.read(config_file)
        creds = cp['sf']
    else:
        cred_names = ['client_id', 'client_secret', 'security_token', 'username', 'password']
        creds = {name: os.getenv(name) for name in cred_names}
    return creds


### Authentication functions

def _get_bearer_token(client_id: str, client_secret: str, security_token: str, username: str, password: str) -> Dict[str, str]:
    """Use username-password flow to request an access token."""
    url = f"https://test.salesforce.com/services/oauth2/token?grant_type=password&client_id={client_id}&client_secret={client_secret}&username={username}&password={password}{security_token}"
    headers= {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(url=url, headers=headers).json()


def _create_bearer_token_header(bearer_dict: Dict[str, str]) -> Dict[str, str]:
    """Use a retrieve bearer token response to create a header dict with the auth token."""
    return {'Authorization': f"{bearer_dict['token_type']} {bearer_dict['access_token']}"}


def get_auth_header(client_id: str, client_secret: str, security_token: str, username: str, password: str) -> Dict[str, str]:
    """Use usernmae-password flow to create a header dict with the auth token."""
    return _create_bearer_token_header(_get_bearer_token(client_id=client_id, client_secret=client_secret, security_token=security_token, username=username, password=password))


### Functions for retrieving client records

# Saleforce object name mapped to urls to retrieve them.
# Assumption that OLI_Client__c is the root parent object and all other objects are children/ancestors, 
# so urls for all non-OLI_Client__c objects are relative query requests.
_sf_object_urls = {'OLI_Client__c': 'https://cs3.salesforce.com/services/data/v43.0/sobjects/OLI_Client__c/{record_id}',
                   'Snapshots_Forms__c': 'https://cs3.salesforce.com/services/data/v43.0/sobjects/OLI_Client__c/{record_id}/Snapshots_Forms__r'
                  }


def get_complete_client_record(oli_client__c_id: str, headers: Dict[str, str]) -> Dict[str, Dict[str, str]]:
    """Function for retrieving a complete client record."""
    record = {}
    for object_name, url in _sf_object_urls.items():
        try:
            record[object_name] = requests.get(url=url.format(record_id=oli_client__c_id), headers=headers).json()
        except Exception as e:
            print(f"Error requesting {object_name} from {url}.")
            print(e)
    return record


