from datetime import datetime

import pytest

from tinvest.utils import isoformat, set_default_headers


def test_set_default_headers(token):
    data = {}
    set_default_headers(data, token)
    assert data == {
        'headers': {'accept': 'application/json', 'Authorization': f'Bearer {token}'}
    }


def test_set_default_headers_with_headers(token):
    data = {
        'headers': {'Authorization': 'Bearer <OTHER_TOKEN>', 'X-Custom-Header': 'value'}
    }
    set_default_headers(data, token)
    assert data == {
        'headers': {
            'accept': 'application/json',
            'Authorization': 'Bearer <OTHER_TOKEN>',
            'X-Custom-Header': 'value',
        }
    }


@pytest.mark.parametrize(
    ('dt', 'expected'),
    [
        ('2000-01-01T00:00:00+00:00', '2000-01-01T00:00:00+00:00'),
        (datetime(2000, 1, 1), '2000-01-01T00:00:00+00:00'),
    ],
)
def test_isoformat(dt, expected):
    assert isoformat(dt) == expected
