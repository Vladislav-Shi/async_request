import json
from typing import List

import aiofiles
from aiohttp import ClientSession, FormData
from bs4 import BeautifulSoup

from app.models import UserInstance, SendFileParams, SendParams
from settings.config import config


async def get_file_urls(session: ClientSession, token: str) -> List[str]:
    """Возвращает все ссылки на фалйы из хранилища.
    Требуется Авторизация"""
    urls = []
    data = FormData()
    data.add_field('token', token)
    data.add_field('page', '0')
    data.add_field('keyword', '')
    async with session.post(config.get_file_manager_url(), data=data) as response:
        response_text = await response.text()
    soup = BeautifulSoup(response_text, 'html.parser')
    files = soup.find_all('div', class_='fm-item col-lg-2 col-md-3 col-sm-6 col-6')
    for file in files:
        urls.append(file.get('data-file'))
    if len(urls) == 0:
        raise ValueError('Не удалось загрузить список файлов')
    return urls


async def login_on_service(session: ClientSession, login: str, password: str, token: str):
    """Авторизация для дополнительных функций API"""
    headers = {
        'Host': 'andwa.ru',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Content-Length': '85',
        'Origin': 'null',
        'Connection': 'keep-alive',
        'Cookie': f'token={token}',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers'
    }
    data = FormData()
    data.add_field('token', token)
    data.add_field('email', login)
    data.add_field('password', password)
    async with session.post(config.get_login_url(), data=data, headers=headers) as response:
        print(response.status)


async def get_user_list(session: ClientSession, token: str) -> List[UserInstance]:
    global request_count
    """Возвращает список пользователей"""
    params = {'access_token': token}
    async with session.get(config.get_access_url(), params=params) as response:
        request_data = await response.json(content_type='text/html')
        request_data = request_data['data']
    result = []
    for i in request_data:
        result.append(UserInstance(**i))
    return result


async def get_user_chat_list(
        session: ClientSession,
        instance_id: str,
        token: str,
        error_instance: list
) -> List:
    """Возвращает кол-во чаты в которых участвует пользователь.
    Требуется Авторизация"""
    params = {
        'instance_id': instance_id,
        'access_token': token
    }
    async with session.get(config.get_chat_url(), params=params) as response:
        response_text = await response.text()
        try:
            response = json.loads(response_text)
            response_text = response['submenu_list']
        except:
            error_instance.append(instance_id)
            async with aiofiles.open('errors.json', mode='a') as f:
                await f.write(f'"{instance_id}": {{"{response_text}"}},\n')

    soup = BeautifulSoup(response_text, 'html.parser')
    chats = soup.find_all('li', class_='wa-submenu-item unread search-list')
    chat_list = []
    for chat in chats:
        chat_list.append(chat.a.get('data-chat-id'))
    return chat_list


async def send_to_user(session: ClientSession, data: SendParams) -> dict:
    """Отправить пользователю сообщение"""
    async with session.get(config.get_send_url(), params=data.dict()) as response:
        return await response.json(content_type='text/html')


async def send_file_to_user(session: ClientSession, data: SendFileParams) -> dict:
    """Отправить пользователю файл"""
    async with session.get(config.get_send_url(), params=data.dict()) as response:
        return await response.json(content_type='text/html')
