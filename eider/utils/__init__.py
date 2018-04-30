from os import path, getcwd
from json import loads, JSONDecodeError

import websockets
import yaml


def load_config_file(test=False):
    conf = open(
        path.join(
            getcwd(), 'development.yml' if test is False else 'test.yml'
        ), 'r'
    )
    try:
        return yaml.load(conf)
    finally:
        conf.close()


def parse(data):
    try:
        return loads(data)
    except JSONDecodeError:
        return


async def transfer(uri, payload):
    async with websockets.connect(uri) as websocket:
        return await websocket.send(bytes(payload))
