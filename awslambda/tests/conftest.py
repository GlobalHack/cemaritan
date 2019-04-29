import json
import os
import pytest
from pathlib import Path

test_path = Path.cwd()

try:
    os.unlink(test_path.joinpath("api/models"))
except:
    os.symlink(test_path.joinpath("models"), test_path.joinpath("api/models"))


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
