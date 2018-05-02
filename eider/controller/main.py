import json
import asyncio
from asyncio.queues import QueueEmpty

import websockets

tasks = asyncio.Queue()


async def consumer(websocket):
    async for job in websocket:
        await tasks.put(job)


async def producer(websocket):
    while True:
        try:
            task = await tasks.get()
            await do_task(websocket, task)
        except QueueEmpty:
            continue


async def do_task(websocket, task):
    pass


async def digest_task(task):
    payload = json.loads(task)
    # if task == json.loads(task)


async def worker(websocket, path):
    consumer_task = asyncio.ensure_future(consumer(websocket))
    producer_task = asyncio.ensure_future(producer(websocket))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()


if __name__ == '__main__':
    start_server = websockets.serve(worker, '127.0.0.1', 5678)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
