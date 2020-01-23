import pytest

from tinvest import (
    Empty,
    LimitOrderRequest,
    LimitOrderResponse,
    OperationType,
    OrdersApi,
    OrdersResponse,
)


@pytest.fixture()
def api_client(http_client):
    return OrdersApi(http_client)


def test_orders_get(api_client, http_client):
    api_client.orders_get()
    http_client.request.assert_called_once_with(
        'GET', '/orders', response_model=OrdersResponse
    )


def test_orders_limit_order_post(api_client, http_client, figi):
    body = LimitOrderRequest(lots=3, operation=OperationType.buy, price=13.5)
    api_client.orders_limit_order_post(figi, body)
    http_client.request.assert_called_once_with(
        'POST',
        '/orders/limit-order',
        response_model=LimitOrderResponse,
        params={'figi': figi},
        data=body.json(by_alias=True),
    )


def test_orders_cancel_post(api_client, http_client):
    order_id = 'some_order_id'
    api_client.orders_cancel_post(order_id)
    http_client.request.assert_called_once_with(
        'POST', '/orders/cancel', response_model=Empty, params={'orderId': order_id}
    )
