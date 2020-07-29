# pylint:disable=redefined-outer-name
import pytest

from tinvest import UserAccountsResponse, UserApi


@pytest.fixture()
def api_client(http_client):
    return UserApi(http_client)


def test_accounts_get(api_client, http_client):
    api_client.accounts_get()
    http_client.request.assert_called_once_with(
        'GET', '/user/accounts', response_model=UserAccountsResponse
    )
