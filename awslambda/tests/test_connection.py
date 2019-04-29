import pytest

from api.connection import connections, get_connection


def test_connections_function(connections_event, sample_connections_response):
    assert connections(connections_event, None) == sample_connections_response


def test_connection_single_function(
    connection_single_event, sample_connection_single_response
):
    assert (
        get_connection(connection_single_event, None)
        == sample_connection_single_response
    )
