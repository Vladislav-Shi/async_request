import asyncio
import itertools
import urllib.parse
from typing import List, TypedDict, Set

import aiofiles
import aiohttp
import pandas

from v1.settings import config


class SendParams(TypedDict):
    number: str
    type: str
    message: str
    instance_id: str
    access_token: str


def generate_send_url_params(data: dict) -> (List[SendParams], Set):
    params_list = []
    combinations = []
    count_data = len(data)
    comb = [i for i in range(0, count_data)]
    com_set = itertools.combinations(comb, 2)
    for i in com_set:
        params: SendParams = {
            'number': data['name'][i[0]],
            'type': 'text',
            'message': urllib.parse.quote(config.config.TEXT),
            'instance_id': data['token'][i[1]],
            'access_token': config.config.TOKEN
        }
        params_list.append(params)
        combinations.append(i)

    return params_list, combinations


async def get_send_data(params: SendParams, session, combinations, i):
    async with session.get(config.get_send_url(), params=params) as response:
        async with aiofiles.open(config.config.OUTPUT, mode='a') as f:
            json_data = await response.json(content_type='text/html')
            try:
                await f.write(f'{i} - {combinations} - body: {json_data["status"]}\n')
            except TypeError:
                await f.write(f'ERROR for: {i}, {combinations}, JSON is None')


async def main():
    tasks = []
    connector = aiohttp.TCPConnector(limit=config.config.LIMIT, keepalive_timeout=600)
    async with aiohttp.ClientSession(connector=connector, trust_env=True, ) as session:
        params = {'access_token': config.config.TOKEN}
        async with session.get(config.get_access_url(), params=params) as response:
            request_data = await response.json(content_type='text/html')
            request_data = pandas.json_normalize(request_data['data'])
        params_list, combinations = generate_send_url_params(request_data)

        async with aiofiles.open(config.config.OUTPUT, mode='w') as f:
            await f.write('')

        for i in range(len(params_list)):
            task = asyncio.ensure_future(get_send_data(params_list[i], session, combinations[i], i))
            tasks.append(task)
            if i % config.config.LIMIT == 0:
                responses = await asyncio.gather(*tasks)
                tasks.clear()
        responses = await asyncio.gather(*tasks)
