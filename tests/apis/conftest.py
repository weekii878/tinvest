import pytest


@pytest.fixture()
def http_client(mocker):
    return mocker.Mock()
