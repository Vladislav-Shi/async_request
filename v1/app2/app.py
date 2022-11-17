import asyncio
from random import randint
from typing import List

import aiofiles
import aiohttp

from v1.settings.config import config, get_send_url, get_access_url
from v1.settings.models import DialogUser


def splitting_via_pairs(data: List[dict]) -> List[DialogUser]:
    result = []
    while len(data):
        user_from = data.pop()
        if len(data):
            user_to = data.pop()
            result.append(DialogUser(
                from_user_name=user_from['name'],
                to_user_name=user_to['name'],
                from_user_token=user_from['token'],
                to_user_token=user_to['token']
            ))
    return result


def generate_send_params(from_user: str, to_user: str, messages: str) -> dict:
    return {
        'number': to_user,
        'type': 'text',
        'message': messages,
        'instance_id': from_user,
        'access_token': config.TOKEN
    }


async def create_dialog(session, dialog: DialogUser, dialog_size: int):
    async with aiofiles.open(config.OUTPUT, mode='a') as f:
        await f.write(f'{dialog.from_user_name} - {dialog.to_user_name} - count messages {dialog_size}\n')
    for i in range(dialog_size):
        params = generate_send_params(
            messages=config.TEXT,
            from_user=dialog.from_user_token,
            to_user=dialog.to_user_name
        )
        async with session.get(get_send_url(), params=params) as response:
            pass
        params = generate_send_params(
            messages=config.TEXT,
            from_user=dialog.to_user_token,
            to_user=dialog.from_user_name
        )
        async with session.get(get_send_url(), params=params) as response:
            pass


async def main():
    async with aiofiles.open(config.OUTPUT, mode='w') as f:
        await f.write('')
    tasks = []
    connector = aiohttp.TCPConnector(limit=config.LIMIT)
    async with aiohttp.ClientSession(connector=connector, trust_env=True) as session:
        params = {'access_token': config.TOKEN}
        async with session.get(get_access_url(), params=params) as response:
            request_data = await response.json(content_type='text/html')

        request_data = request_data['data']
            pairs = splitting_via_pairs(request_data)
        print('кол-во диалогов:', len(pairs))
        for i in range(len(pairs)):
            task = asyncio.ensure_future(create_dialog(
                session=session,
                dialog=pairs[i],
                dialog_size=randint(config.MIN_DIALOG_SIZE, config.MAX_DIALOG_SIZE)
            )
            )
            tasks.append(task)
            if i % config.LIMIT == 0:
                responses = await asyncio.gather(*tasks)
                tasks.clear()

        responses = await asyncio.gather(*tasks)
