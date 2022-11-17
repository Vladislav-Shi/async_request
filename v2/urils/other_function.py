import itertools
import json
import random
import urllib.parse
from random import randint
from typing import List, Set

import aiofiles
from aiohttp import ClientSession

from v2.app.models import UserInstance, SendParams, DialogUser, SendFileParams
from v2.settings.config import config
from v2.urils import andwa_request
from v2.urils.andwa_request import send_to_user, send_file_to_user, get_file_urls
from v2.urils.data_generation import generate_send_params, generate_send_params_with_file


async def user_chat_log(session: ClientSession, user: UserInstance, error_instance: list):
    """Данная функция служит для асинхронной обработки сразу пачки запросов"""
    chats = await andwa_request.get_user_chat_list(
        session=session,
        instance_id=user.token,
        token=config.TOKEN,
        error_instance=error_instance
    )
    async with aiofiles.open('dialog.json', mode='a') as f:
        await f.write(f'"{user.name}":{{"count": {len(chats)}, "dialogs": {json.dumps(chats)} }},\n')


def generate_send_url_params(data: List[UserInstance]) -> (List[SendParams], Set):
    params_list: List[SendParams] = []
    combinations = []
    count_data = len(data)
    comb = [i for i in range(0, count_data)]
    com_set = itertools.combinations(comb, 2)
    for i in com_set:
        params = SendParams(
            number=data[i[0]].name,
            message=urllib.parse.quote_plus(config.TEXT),
            instance_id=data[i[1]].token,
            access_token=config.TOKEN
        )
        params_list.append(params)
        combinations.append(i)

    return params_list, combinations


async def get_send_data(params: SendParams, session: ClientSession, combinations: Set, i: int):
    json_data = await send_to_user(session=session, data=params)
    async with aiofiles.open(config.OUTPUT, mode='a') as f:
        try:
            await f.write(f'{i} - {combinations} - body: {json_data["status"]}\n')
        except TypeError:
            await f.write(f'ERROR for: {i}, {combinations}, JSON is None')


async def send_message(session: ClientSession, to_user: str, from_user: str, file_url: str):
    if randint(0, 100) < config.IMAGE_MESSAGE_CHANCE:
        file_name = file_url.split('/')[-1]
        params = generate_send_params_with_file(
            messages=config.TEXT,
            from_user=from_user,
            to_user=to_user,
            file_url=file_url,
            file_name=file_name
        )
        return await send_file_to_user(session=session, data=params, )
    else:
        params = generate_send_params(
            messages=config.TEXT,
            from_user=from_user,
            to_user=to_user,
        )
        return await send_to_user(session=session, data=params)


async def create_dialog(session: ClientSession, dialog: DialogUser, dialog_size: int, file_list: list):
    task = []
    async with aiofiles.open(config.OUTPUT, mode='a') as f:
        await f.write(f'{dialog.from_user_name} - {dialog.to_user_name} - count messages {dialog_size}\n')
    for i in range(dialog_size):
        await send_message(
            session=session,
            to_user=dialog.to_user_name,
            from_user=dialog.from_user_token,
            file_url=random.choice(file_list)
        )
        await send_message(
            session=session,
            to_user=dialog.to_user_token,
            from_user=dialog.from_user_name,
            file_url=random.choice(file_list)
        )
