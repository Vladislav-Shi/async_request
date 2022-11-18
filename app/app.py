import asyncio
from random import randint

import aiofiles
import aiohttp
from tortoise import Tortoise

from settings.config import config, TORTOISE_ORM
from urils import andwa_request
from urils.andwa_request import get_file_urls, login_on_service
from urils.other_function import user_chat_log, generate_send_url_params, get_send_data, create_dialog, get_dialog_list


async def init_bd():
    await Tortoise.init(config=TORTOISE_ORM)


async def get_users_chats():
    """Записывает в файл все о количествах чатов каждого пользователя системы"""
    tasks = []
    error_instance = []
    connector = aiohttp.TCPConnector(limit=config.LIMIT, keepalive_timeout=600)
    async with aiohttp.ClientSession(connector=connector, trust_env=True, ) as session:
        await andwa_request.login_on_service(
            session=session,
            token='1578bda095eee55eb0b1d993553697d7',
            login=config.LOGIN,
            password=config.PASSWORD
        )
        users = await andwa_request.get_user_list(
            session=session,
            token=config.TOKEN
        )
        async with aiofiles.open(config.OUTPUT, mode='w') as f:
            await f.write('{\n')
        print('USER count:', len(users))
        for i in range(len(users)):
            task = asyncio.ensure_future(user_chat_log(session=session, user=users[i], error_instance=error_instance))
            tasks.append(task)
            if i % 50 == 0:
                responses = await asyncio.gather(*tasks)
                tasks.clear()
        responses = await asyncio.gather(*tasks)
        print('Не удалось обработать:', len(error_instance))
        async with aiofiles.open(config.OUTPUT, mode='a') as f:
            await f.write('}\n')


async def send_combination_request():
    """Отправляет сообщения по всем возможным комбинациям"""
    tasks = []
    connector = aiohttp.TCPConnector(limit=config.LIMIT, keepalive_timeout=600)
    async with aiohttp.ClientSession(connector=connector, trust_env=True, ) as session:
        users = await andwa_request.get_user_list(
            session=session,
            token=config.TOKEN
        )
        params_list, combinations = generate_send_url_params(users)

        async with aiofiles.open(config.OUTPUT, mode='w') as f:
            await f.write('')

        for i in range(len(params_list)):
            task = asyncio.ensure_future(get_send_data(params_list[i], session, combinations[i], i))
            tasks.append(task)
            if i % config.LIMIT == 0:
                responses = await asyncio.gather(*tasks)
                tasks.clear()
        responses = await asyncio.gather(*tasks)


async def create_users_dialog():
    await init_bd()

    async with aiofiles.open(config.OUTPUT, mode='w') as f:
        await f.write('')
    tasks = []
    connector = aiohttp.TCPConnector(limit=config.LIMIT)
    async with aiohttp.ClientSession(connector=connector, trust_env=True) as session:
        users = await andwa_request.get_user_list(
            session=session,
            token=config.TOKEN
        )
        dialogs = await get_dialog_list(users=users)
        print('кол-во диалогов:', len(dialogs))
        await login_on_service(session=session, login=config.LOGIN, password=config.PASSWORD, token=config.INNER_TOKEN)
        file_list = await get_file_urls(session=session, token=config.INNER_TOKEN)
        print('Кол-во медиа файлов:', len(file_list))
        for i in range(len(dialogs)):
            task = asyncio.ensure_future(
                create_dialog(
                    session=session,
                    dialog=dialogs[i],
                    dialog_size=randint(config.MIN_DIALOG_SIZE, config.MAX_DIALOG_SIZE),
                    file_list=file_list
                )
            )
            tasks.append(task)
            if i % config.LIMIT == 0:
                responses = await asyncio.gather(*tasks)
                tasks.clear()

        responses = await asyncio.gather(*tasks)
        print('кол-во совершенных запросов:')

