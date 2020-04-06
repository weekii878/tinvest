# pylint: disable=unused-variable
import asynctest
import pytest

from tinvest import CandleResolution, Streaming, StreamingApi, StreamingEvents


@pytest.fixture()
def ws():
    _ws = asynctest.Mock(autospec=True)
    _ws.send_json = asynctest.CoroutineMock(autospec=True)
    return _ws


@pytest.fixture()
def streaming_events():
    return StreamingEvents()


@pytest.fixture()
def streaming_api(ws):
    return StreamingApi(ws)


@pytest.fixture()
def _streaming_api_with_state(streaming_api):
    streaming_api._state = {'some_key': True}


@pytest.fixture()
def fake_handler(streaming_events, mocker):
    func = mocker.Mock(autospec=True)
    streaming_events.startup()(func)
    streaming_events.candle()(func)
    streaming_events.orderbook()(func)
    streaming_events.instrument_info()(func)
    streaming_events.error()(func)
    streaming_events.cleanup()(func)
    return func


@pytest.fixture()
def _handlers(streaming_events):
    @streaming_events.startup()
    def startup():
        pass

    @streaming_events.candle()
    def candle():
        pass

    @streaming_events.orderbook()
    def orderbook():
        pass

    @streaming_events.instrument_info()
    def instrument_info():
        pass

    @streaming_events.error()
    def error():
        pass

    @streaming_events.cleanup()
    def cleanup():
        pass


@pytest.yield_fixture()
async def streaming(token, streaming_events):
    s = Streaming(token).add_handlers(streaming_events)
    yield s
    await s._session.close()


@pytest.mark.usefixtures('_handlers')
def test_handlers_count(streaming_events):
    assert len(streaming_events.handlers) == 6


@pytest.mark.usefixtures('_handlers')
def test_handlers_calling(streaming_events):
    for _, handle in streaming_events.handlers:
        handle()  # skip


def test_fake_handlers_calling(streaming_events, fake_handler):
    for _, handle in streaming_events.handlers:
        handle()

    assert fake_handler.call_count == 6


@pytest.mark.usefixtures('_streaming_api_with_state')
def test_streaming_api_state(streaming_api):
    assert streaming_api['some_key']


@pytest.mark.usefixtures('_streaming_api_with_state')
def test_streaming_api_state_error(streaming_api):
    with pytest.raises(KeyError):
        assert streaming_api['some_unknown_key']


@pytest.mark.asyncio
@pytest.mark.parametrize('action', ['subscribe', 'unsubscribe'])
async def test_streaming_candle(streaming_api, ws, figi, action):
    await getattr(streaming_api.candle, action)(figi, CandleResolution.min1)
    ws.send_json.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.parametrize('action', ['subscribe', 'unsubscribe'])
async def test_streaming_candle_error(streaming_api, ws, figi, action):
    with pytest.raises(ValueError):
        await getattr(streaming_api.candle, action)(figi, 'invalid data')
    ws.send_json.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize('action', ['subscribe', 'unsubscribe'])
async def test_streaming_orderbook(streaming_api, ws, figi, action):
    await getattr(streaming_api.orderbook, action)(figi, 5)
    ws.send_json.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.parametrize('action', ['subscribe', 'unsubscribe'])
async def test_streaming_instrument_info(streaming_api, ws, figi, action):
    await getattr(streaming_api.instrument_info, action)(figi)
    ws.send_json.assert_called_once()


def test_streaming_without_token():
    with pytest.raises(ValueError):
        Streaming('')


@pytest.mark.usefixtures('_handlers')
@pytest.mark.parametrize(
    'event_name', ['startup', 'candle', 'instrument_info', 'error', 'cleanup']
)
def test_streaming_get_handlers(streaming, event_name):
    assert streaming._get_handlers(event_name)


@pytest.mark.asyncio
async def test_streaming_cleanup(streaming, streaming_api):
    await streaming._cleanup(streaming_api)
