import asyncio
import random

import aiohttp

from v2.settings.config import config
from v2.urils import andwa_request
from v2.urils.andwa_request import login_on_service, get_file_urls
from v2.urils.other_function import send_message


async def main():
    connector = aiohttp.TCPConnector(limit=config.LIMIT)
    async with aiohttp.ClientSession(connector=connector, trust_env=True) as session:
        users = await andwa_request.get_user_list(
            session=session,
            token=config.TOKEN
        )
        await login_on_service(session=session, login=config.LOGIN, password=config.PASSWORD, token=config.TOKEN)
        file_list = await get_file_urls(session=session, token=config.TOKEN)
        print('Кол-во медиа файлов:', len(file_list))
        for i in range(20):
            resp = await send_message(
                session=session,
                from_user='637696C14B52E',
                to_user='79299310244',
                file_url=random.choice(file_list)
            )
            print(resp)
            await asyncio.sleep(3)
            resp = await send_message(
                session=session,
                from_user='637684848C510',
                to_user='77716522089',
                file_url=random.choice(file_list)
            )
            print(resp)
            await asyncio.sleep(2)

asyncio.run(main())
