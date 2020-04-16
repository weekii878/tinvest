from datetime import datetime

import pytest

from tinvest.utils import isoformat, parse_datetime, set_default_headers


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


@pytest.mark.parametrize(
    ('dt', 'expected'),
    [
        ('2000-01-01T00:00:00.12321351Z', datetime(2000, 1, 1, microsecond=123214)),
        ('2000-01-01T00:00:00.123112Z', datetime(2000, 1, 1, microsecond=123112)),
        ('2000-01-01T00:00:00.123Z', datetime(2000, 1, 1, microsecond=123000)),
        ('2000-01-01T00:00:00.0Z', datetime(2000, 1, 1)),
        ('2000-01-01T00:00:00Z', datetime(2000, 1, 1)),
    ],
)
def test_utc_datetime(dt, expected):
    assert parse_datetime(dt) == expected
