# pylint:disable=redefined-outer-name
import pytest

from tinvest import (
    MarketApi,
    OpenApi,
    OperationsApi,
    OrdersApi,
    PortfolioApi,
    SandboxApi,
    UserApi,
)


@pytest.fixture()
def api_client(http_client):
    return OpenApi(http_client)


@pytest.mark.parametrize(
    ('attr', 'type_'),
    [
        ('sandbox', SandboxApi),
        ('orders', OrdersApi),
        ('portfolio', PortfolioApi),
        ('market', MarketApi),
        ('operations', OperationsApi),
        ('user', UserApi),
    ],
)
def test_http_instances(api_client, attr, type_):
    assert isinstance(getattr(api_client, attr), type_)
