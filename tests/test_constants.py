from tinvest.constants import PRODUCTION, SANDBOX, STREAMING


def test_production():
    assert PRODUCTION == 'https://api-invest.tinkoff.ru/openapi'


def test_sandbox():
    assert SANDBOX == 'https://api-invest.tinkoff.ru/openapi/sandbox'


def test_steaming():
    assert STREAMING == 'wss://api-invest.tinkoff.ru/openapi/md/v1/md-openapi/ws'
