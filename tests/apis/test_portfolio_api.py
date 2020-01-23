import pytest

from tinvest import PortfolioApi, PortfolioCurrenciesResponse, PortfolioResponse


@pytest.fixture()
def api_client(http_client):
    return PortfolioApi(http_client)


def test_portfolio_get(api_client, http_client):
    api_client.portfolio_get()
    http_client.request.assert_called_once_with(
        'GET', '/portfolio', response_model=PortfolioResponse
    )


def test_portfolio_currencies_get(api_client, http_client):
    api_client.portfolio_currencies_get()
    http_client.request.assert_called_once_with(
        'GET', '/portfolio/currencies', response_model=PortfolioCurrenciesResponse,
    )
