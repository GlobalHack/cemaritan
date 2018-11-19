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
import datetime

import requests

from customtyping import *

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
    """Use username-password flow to create a header dict with the auth token."""
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
            response_json = requests.get(url=url.format(record_id=oli_client__c_id), headers=headers).json()
            if object_name != 'OLI_Client__c':
                response_json = response_json['records']
            record[object_name] = response_json
        except Exception as e:
            print(f"Error requesting {object_name} from {url}.")
            print(e)
    return record


### Get recently updated records

updated_url = 'https://cs3.salesforce.com/services/data/v29.0/sobjects/{object_type}/updated/'

def _format_dt(dt):
    """Format a datetime to match SF query parameters format."""
    dt_s = str(dt)
    return dt_s.replace(' ', 'T')[:-7] + '+00'
    

def _get_parameters_for_recent_times(minutes: int=None):
    """Generate parameters dict for retrieving updated SF records.
    
    Parameters
    ----------
    minutes : int
        Minutes ago to start retrieving records.
    """
    now = datetime.datetime.utcnow()
    end = now + datetime.timedelta(minutes=5)
    start = now - datetime.timedelta(minutes=minutes)
    return {'start': _format_dt(start), 'end': _format_dt(end)}


def get_recently_changed_object_ids(headers: Dict, object_type: str='OLI_Client__c', minutes: int=5) -> List[str]:
    """Get recently changed SF objects.
    
    Parameters
    ----------
    headers : Dict
        Headers for request that must include the auth header.
    object_type : str
        SF object type requested.
    minutes : int
        Number of minutes back to look for updates.
    """
    _url = updated_url.format(object_type=object_type)
    parameters = _get_parameters_for_recent_times(minutes=minutes)
    response = requests.get(url=_url, params=parameters, headers=headers)
    if response.status_code != 200:
        raise ValueError(response.reason)
    return response.json()['ids']
    

def get_recent_records(headers: Dict, object_type: str='OLI_Client__c', minutes: int=5) -> List[SfRecord]:
    """Get a list of SF Objects that have been created/updated in last `minutes` minutes.
    
    Parameters
    ----------
    headers : Dict
        Headers for request that must include the auth header.
    object_type : str
        SF object type requested.
    minutes : int
        Number of minutes back to look for updates.
    """
    ids = get_recently_changed_object_ids(minutes=minutes, headers=headers)
    updated = []
    for id_ in ids:
        updated.append(get_complete_client_record(oli_client__c_id=id_, headers=headers))
    return updated
