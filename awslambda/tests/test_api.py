import json

import pytest

from api.connection import connections, get_connection
from api.transfer import transfers, get_transfer, create_transfer, delete_transfer, get_frequencies_list, update_transfer
from api.history import histories, get_history
from api.mapping import mappings, get_mapping
from api.user import get_user
from api.organization import organizations, get_organization
from api.download import downloads, get_download, get_download_link
from api.upload import get_upload_link, create_upload, get_upload

import logging

for name in logging.Logger.manager.loggerDict.keys():
    if ('boto' in name) or ('urllib3' in name) or ('s3transfer' in name) or ('boto3' in name) or ('botocore' in name) or ('nose' in name):
        logging.getLogger(name).setLevel(logging.CRITICAL)


### Connections
def test_connections_function(connections_event, sample_connections_response):
    assert connections(connections_event, None) == sample_connections_response


def test_connection_single_function(
    connection_single_event, sample_connection_single_response
):
    assert (
        get_connection(connection_single_event, None)
        == sample_connection_single_response
    )
    

# ### Transfers
def test_transfers_function(transfers_event, sample_transfers_response):
    # assert transfers(transfers_event, None) == sample_transfers_response
    result = transfers(transfers_event, None)
    assert result.keys() == sample_transfers_response.keys()
    result_body = json.loads(result['body'])
    sample_body = json.loads(sample_transfers_response['body'])
    assert len(result_body) == len(sample_body)


def test_transfer_single_function(
    transfer_single_event, sample_transfer_single_response
):
    assert get_transfer(transfer_single_event, None) == sample_transfer_single_response


# def test_transfer_single_update_response

def test_transfer_single_update_function(sample_transfer_single_update_event, 
    sample_transfer_single_update_response,
    transfer_single_event,
    sample_transfer_single_response_after_update):
    assert update_transfer(sample_transfer_single_update_event, None) == sample_transfer_single_update_response
    assert get_transfer(transfer_single_event, None) == sample_transfer_single_response_after_update


def test_transfer_single_create_function(
    sample_transfer_single_create_event, sample_transfer_single_create_response, transfer_single_event
):
    _id = json.loads(create_transfer(sample_transfer_single_create_event, None)['body'])['uid']
    transfer_single_event['pathParameters']['transfer_id'] = _id
    body = json.loads(sample_transfer_single_create_response['body'])
    body['uid'] = _id
    sample_transfer_single_create_response['body'] = json.dumps(body)
    assert (
        get_transfer(transfer_single_event, None)
        == sample_transfer_single_create_response
    )




### Histories
# def test_histories_function(histories_event, sample_histories_response):
#     assert histories(histories_event, None) == sample_histories_response


def test_frequencies_list(sample_frequencies_list_response):
    assert get_frequencies_list(None, None) == sample_frequencies_list_response
    

def test_history_single_function(history_single_event, sample_history_single_response):
    assert get_history(history_single_event, None) == sample_history_single_response


### Mappings
def test_mappings_function(mappings_event, sample_mappings_response):
    assert mappings(mappings_event, None) == sample_mappings_response


def test_mapping_single_function(mapping_single_event, sample_mapping_single_response):
    assert get_mapping(mapping_single_event, None) == sample_mapping_single_response


# ### Users
# def test_users_function(users_event, sample_users_response):
#     assert users(users_event, None) == sample_users_response


def test_user_single_function(user_single_event, sample_user_single_response):
    assert get_user(user_single_event, None) == sample_user_single_response


### Organizations
def test_organizations_function(organizations_event, sample_organizations_response):
    assert organizations(organizations_event, None) == sample_organizations_response


def test_organization_single_function(
    organization_single_event, sample_organization_single_response
):
    assert (
        get_organization(organization_single_event, None)
        == sample_organization_single_response
    )


### Downloads
def test_downloads_function(downloads_event, sample_downloads_response):
    assert downloads(downloads_event, None) == sample_downloads_response


def test_download_single_function(
    download_single_event, sample_download_single_response
):
    assert get_download(download_single_event, None) == sample_download_single_response


def test_download_link_function(download_single_event, sample_download_link_response):
    result = get_download_link(download_single_event, None)
    body = json.loads(result['body'])
    body["download_link"] = ""
    result['body'] = json.dumps(body)
    assert result == sample_download_link_response
    #assert get_download_link(download_single_event, None) == sample_download_link_response


# Upload
def test_upload_function(upload_single_create_event, sample_upload_single_event, sample_upload_single_response):
    _id = json.loads(create_upload(upload_single_create_event, None)['body'])['uid']
    # print(_id)
    sample_upload_single_event['pathParameters']['upload_id'] = _id
    body = json.loads(sample_upload_single_response['body'])
    body['uid'] = _id
    sample_upload_single_response['body'] = json.dumps(body)
    response = get_upload(sample_upload_single_event, None)
    d = json.loads(response['body'])
    del d['expiration_datetime']
    del d['created_datetime']
    response['body'] = json.dumps(d)
    # assert (
    #     response
    #     == sample_upload_single_response
    # )
    assert(response.keys() == sample_upload_single_response.keys())
    assert(sorted(json.loads(response['body']).keys()) == sorted(json.loads(sample_upload_single_response['body']).keys()))
    keys = sorted(json.loads(response['body']).keys())
    for k in keys:
        assert(json.loads(response['body'])[k] == json.loads(sample_upload_single_response['body'])[k])