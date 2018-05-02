import asyncio
from asyncio.queues import QueueEmpty

import websockets

tasks = asyncio.Queue()


async def consumer(websocket):
    async for message in websocket:
        print(message)
        await tasks.put(message)


async def producer(websocket):
    while True:
        try:
            task = await tasks.get()
            print(task)
            await do_task(websocket, task)
        except QueueEmpty:
            continue


async def do_task(websocket, task):
    await websocket.send(task)


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
