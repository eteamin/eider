import asyncio
import websockets

from eider.utils import parse


async def setup():
    pass

async def teardown():
    pass


async def test_send_text_message(uri):
    async with websockets.connect(uri) as websocket:
        resp = await parse(websocket.send("Hello"))
        assert resp.get('ack') is True


asyncio.get_event_loop().run_until_complete(
    test_send_text_message('ws://localhost:8765'))
