# pylint:disable=redefined-outer-name
import pytest

from tinvest.base_client import BaseClient
from tinvest.constants import PRODUCTION, SANDBOX


def test_create_client(token):
    session = object()
    client = BaseClient(token, session=session)

    assert client._base_url == PRODUCTION  # pylint:disable=protected-access
    assert client.session is session


def test_create_client_with_empty_token():
    with pytest.raises(ValueError, match='^Token can not be empty$'):
        BaseClient('')


def test_create_client_for_sandbox(token):
    client = BaseClient(token, use_sandbox=True)

    assert client._base_url == SANDBOX  # pylint:disable=protected-access


def test_create_client_without_session(token):
    client = BaseClient(token)
    with pytest.raises(AttributeError):
        assert not client.session
