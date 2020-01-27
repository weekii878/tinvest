import pytest


@pytest.fixture()
def token():
    return '<TOKEN>'


@pytest.fixture()
def figi():
    return 'BBG0013HGFT4'


@pytest.fixture()
def broker_account_id():
    return 'some_broker_account_id'
