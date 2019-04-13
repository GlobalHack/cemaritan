import pytest

from api.connection import connections


def test_connections_function(sample_event, sample_connection_response):
    assert connections(sample_event, None) == sample_connection_response
