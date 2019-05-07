import pytest

from api.connection import connections, get_connection
from api.transfer import transfers, get_transfer, create_transfer
from api.history import histories, get_history
from api.mapping import mappings, get_mapping
from api.user import users, get_user
from api.organization import organizations, get_organization


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

### Transfers
def test_transfers_function(transfers_event, sample_transfers_response):
    assert transfers(transfers_event, None) == sample_transfers_response


def test_transfer_single_function(
    transfer_single_event, sample_transfer_single_response
):
    assert (
        get_transfer(transfer_single_event, None)
        == sample_transfer_single_response
    )


def test_transfer_single_create_function(
    sample_transfer_single_create_event, sample_transfer_single_create_response
):
    assert (
        create_transfer(sample_transfer_single_create_event, None)
        == sample_transfer_single_create_response
    )


# need pytest -s flag to see print statements
# def test_print(
#     sample_transfer_single_create_event, sample_transfer_single_create_response):
#     # print(create_transfer(sample_transfer_single_create_event, None))
    
#     print(create_transfer(sample_transfer_single_create_event, None))


### Histories
def test_histories_function(histories_event, sample_histories_response):
    assert histories(histories_event, None) == sample_histories_response


def test_history_single_function(
    history_single_event, sample_history_single_response
):
    assert (
        get_history(history_single_event, None)
        == sample_history_single_response
    )


### Mappings
def test_mappings_function(mappings_event, sample_mappings_response):
    assert mappings(mappings_event, None) == sample_mappings_response


def test_mapping_single_function(
    mapping_single_event, sample_mapping_single_response
):
    assert (
        get_mapping(mapping_single_event, None)
        == sample_mapping_single_response
    )


### Users
def test_users_function(users_event, sample_users_response):
    assert users(users_event, None) == sample_users_response


def test_user_single_function(
    user_single_event, sample_user_single_response
):
    assert (
        get_user(user_single_event, None)
        == sample_user_single_response
    )


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