import asyncio
from gino import Gino

db = Gino()


async def main():
    await db.set_bind('postgresql://localhost/gino')
    await db.gino.create_all()

    # further code goes here

    await db.pop_bind().close()


asyncio.get_event_loop().run_until_complete(main())
