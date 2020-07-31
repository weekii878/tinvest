# pylint:disable=redefined-outer-name
# pylint:disable=unused-argument
# pylint:disable=unused-variable
# pylint:disable=protected-access
import aiohttp
import asynctest
import pytest

from tinvest import CandleResolution, Streaming, StreamingApi, StreamingEvents


@pytest.fixture()
def ws():
    return asynctest.Mock(aiohttp.ClientWebSocketResponse, autospec=True)


@pytest.fixture()
def session():
    return asynctest.Mock(aiohttp.ClientSession, autospec=True)


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
    def startup(*args):
        pass

    @streaming_events.candle()
    def candle(*args, **kwargs):
        pass

    @streaming_events.orderbook()
    def orderbook(*args, **kwargs):
        pass

    @streaming_events.instrument_info()
    def instrument_info(*args, **kwargs):
        pass

    @streaming_events.error()
    def error(*args, **kwargs):
        pass

    @streaming_events.cleanup()
    def cleanup(*args):
        pass


@pytest.fixture()
async def streaming(token, streaming_events, session):
    return Streaming(token, session=session).add_handlers(streaming_events)


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
    ws.send_json.assert_called_once_with(
        {'event': f'candle:{action}', 'figi': figi, 'interval': CandleResolution.min1}
    )


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


@pytest.mark.asyncio
async def test_streaming_without_token():
    with pytest.raises(ValueError, match='^Token can not be empty$'):
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


@pytest.mark.asyncio
async def test_streaming_server_time_in_handler():
    def func(api, payload, server_time):
        pass

    Streaming('TOKEN').add_handlers([('some_event', func)])

    assert func.receive_server_time__  # pylint:disable=no-member


def test_streaming_events(streaming_events):
    @streaming_events.candle()
    def some_func():
        return True

    assert some_func.__name__ == 'some_func'
    assert some_func()
