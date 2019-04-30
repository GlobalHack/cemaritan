# cd /awslambda
# python -m pytest

import json
import os
import pytest
from pathlib import Path

test_path = Path.cwd()

try:
    os.unlink(test_path.joinpath("api/models"))
except:
    pass
os.symlink(test_path.joinpath("models"), test_path.joinpath("api/models"))

try:
    os.unlink(test_path.joinpath("api/library"))
except:
    pass
os.symlink(test_path.joinpath("library"), test_path.joinpath("api/library"))

### Connections
@pytest.fixture()
def connections_event():
    return {"pathParameters": {"organization_id": "1"}}


@pytest.fixture()
def connection_single_event():
    return {"pathParameters": {"organization_id": "1", "connection_id": "1"}}


@pytest.fixture()
def sample_connections_response():
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": '[{"uid": 1, "organization": 1, "name": "SF", "createddate": "2019-03-09 20:42:03", "createdby": 1, "type": "A", "connectioninfo": "{conn string}"}, {"uid": 2, "organization": 1, "name": "CW", "createddate": "2019-03-10 04:42:03", "createdby": 1, "type": "B", "connectioninfo": "{conn string}"}, {"uid": 6, "organization": 1, "name": "Secure Download", "createddate": "2019-03-23 20:42:03", "createdby": 0, "type": "F", "connectioninfo": "0"}]',
    }


@pytest.fixture()
def sample_connection_single_response():
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": '{"uid": 1, "organization": 1, "name": "SF", "createddate": "2019-03-09 20:42:03", "createdby": 1, "type": "A", "connectioninfo": "{conn string}"}',
    }

### Transfers
@pytest.fixture()
def transfers_event():
    return {"pathParameters": {"organization_id": "1"}}


@pytest.fixture()
def transfer_single_event():
    return {"pathParameters": {"organization_id": "1", "transfer_id": "1"}}


@pytest.fixture()
def sample_transfers_response():
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": '[{"uid": 1, "name": "CW to SF", "organization": "OLI", "createddate": "2019-03-20 20:42:03", "source": "CW", "sourcemapping": "CW to HUD", "destination": "SF", "destinationmapping": "SF to HUD", "active": "TRUE", "starttime": "2019-03-13 20:42:03", "frequency": "1 day"}, {"uid": 2, "name": "SF to CW", "organization": "OLI", "createddate": "2019-03-13 20:42:03", "source": "SF", "sourcemapping": "SF to HUD", "destination": "CW", "destinationmapping": "CW to HUD", "active": "FALSE", "starttime": "2019-03-13 20:42:03", "frequency": "1 hour"}]',
    }


@pytest.fixture()
def sample_transfer_single_response():
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": '{"uid": 1, "name": "CW to SF", "organization": "OLI", "createddate": "2019-03-20 20:42:03", "source": "CW", "sourcemapping": "CW to HUD", "destination": "SF", "destinationmapping": "SF to HUD", "active": "TRUE", "starttime": "2019-03-13 20:42:03", "frequency": "1 day"}'
    }


### Histories
@pytest.fixture()
def histories_event():
    return {"pathParameters": {"organization_id": "1"}}


@pytest.fixture()
def history_single_event():
    return {"pathParameters": {"organization_id": "1", "history_id": "2"}}


@pytest.fixture()
def sample_histories_response():
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": '[{"uid": 2, "type": "Transfer", "action": null, "date": "2019-03-20 20:42:03", "createdbyuser": 1, "name": null, "details": null, "sourceuid": 0, "organization": 1}, {"uid": 3, "type": "Transfer", "action": null, "date": "2019-03-20 20:42:03", "createdbyuser": 1, "name": null, "details": null, "sourceuid": 0, "organization": 1}, {"uid": 4, "type": "Transfer", "action": "Action B", "date": "2019-03-20 20:42:03", "createdbyuser": 1, "name": null, "details": null, "sourceuid": 0, "organization": 1}]',
    }


@pytest.fixture()
def sample_history_single_response():
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": '{"uid": 2, "type": "Transfer", "action": null, "date": "2019-03-20 20:42:03", "createdbyuser": 1, "name": null, "details": null, "sourceuid": 0, "organization": 1}'
    }



### Mappings
@pytest.fixture()
def mappings_event():
    return {"pathParameters": {"organization_id": "1"}}


@pytest.fixture()
def mapping_single_event():
    return {"pathParameters": {"organization_id": "1", "mapping_id": "1"}}


@pytest.fixture()
def sample_mappings_response():
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": '[{"uid": 1, "organization": 1, "name": "SF to HUD", "mappinginfo": "{}", "startformat": "csv", "endformat": "json", "numoftransfers": 1}, {"uid": 2, "organization": 1, "name": "CW to HUD", "mappinginfo": "{}", "startformat": "csv", "endformat": "json", "numoftransfers": 2}]',
    }


@pytest.fixture()
def sample_mapping_single_response():
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": '{"uid": 1, "organization": 1, "name": "SF to HUD", "mappinginfo": "{}", "startformat": "csv", "endformat": "json", "numoftransfers": 1}'
    }


### Users
@pytest.fixture()
def users_event():
    return {"pathParameters": {"organization_id": "1"}}


@pytest.fixture()
def user_single_event():
    return {"pathParameters": {"organization_id": "1", "user_id": "1"}}


@pytest.fixture()
def sample_users_response():
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": '[{"uid": 1, "name": "Matt", "createddate": "2019-03-10 10:42:03", "organization": 1}]',
    }


@pytest.fixture()
def sample_user_single_response():
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": '{"uid": 1, "name": "Matt", "createddate": "2019-03-10 10:42:03", "organization": 1}'
    }


### Organizations
@pytest.fixture()
def organizations_event():
    return {"pathParameters": {"organization_id": "1"}}


@pytest.fixture()
def organization_single_event():
    return {"pathParameters": {"organization_id": "1", "organization_id": "1"}}


@pytest.fixture()
def sample_organizations_response():
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": '[{"uid": 1, "name": "OLI", "createddate": "2019-03-13 20:42:03"}, {"uid": 2, "name": "SPC", "createddate": "2019-03-15 01:03:03"}, {"uid": 3, "name": "OLI 2", "createddate": "2019-03-18 20:42:03"}]',
    }


@pytest.fixture()
def sample_organization_single_response():
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": '{"uid": 1, "name": "OLI", "createddate": "2019-03-13 20:42:03"}'
    }






try:
    os.unlink(test_path.joinpath("api/models"))
except:
    pass

try:
    os.unlink(test_path.joinpath("api/library"))
except:
    pass