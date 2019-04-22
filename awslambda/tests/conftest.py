import json
import pytest


@pytest.fixture()
def sample_event():
    return {"body": "test"}


@pytest.fixture()
def sample_connection():
    return [
        {
            "UID": 1,
            "Organization": 1,
            "Name": "SF",
            "CreatedDate": "2019-03-09 20:42:03",
            "CreatedBy": 1,
            "Type": "A",
            "ConnectionInfo": "{conn string}",
        },
        {
            "UID": 2,
            "Organization": 1,
            "Name": "CW",
            "CreatedDate": "2019-03-10 04:42:03",
            "CreatedBy": 1,
            "Type": "B",
            "ConnectionInfo": "{conn string}",
        },
        {
            "UID": 6,
            "Organization": 1,
            "Name": "Secure Download",
            "CreatedDate": "2019-03-23 20:42:03",
            "CreatedBy": 0,
            "Type": "F",
            "ConnectionInfo": 0,
        },
    ]


@pytest.fixture()
def sample_connection_response(sample_connection):
    return {"statusCode": 200, "body": json.dumps(sample_connection)}
