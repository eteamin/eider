import asyncio
from eider.utils import load_config_file, transfer


CONFIGURATION = load_config_file(test=True)


async def test_registration(uri):
    payload = {
        'username': 'test'
    }
    resp = await transfer(uri, payload)
    assert resp.get('ack') is True


asyncio.get_event_loop().run_until_complete(
    test_registration(
        '{}:{}/api/message'.format(
            CONFIGURATION.get('host'),
            CONFIGURATION.get('port')
        )
    )
)
