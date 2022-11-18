import asyncio

from aerich import Command

from settings.config import TORTOISE_ORM


async def main():
    command = Command(tortoise_config=TORTOISE_ORM, app='models')
    await command.init_db(True)
    await command.init()
    await command.migrate()

asyncio.run(main())
