import json
import pytest

from api.connection import connections


@pytest.fixture()
def sample_body():
    return {"body": "test"}


@pytest.fixture()
def sample_connection_response():
    return {
        "statusCode": 200,
        "body": json.dumps(
            [
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
        ),
    }


def test_connections_function(sample_body, sample_connection_response):
    assert connections(sample_body, None) == sample_connection_response
