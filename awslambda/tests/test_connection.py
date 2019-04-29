import pytest

from api.connection import connections


def test_connections_function(connections_event, sample_connection_response):
    assert connections(connections_event, None) == sample_connection_response
