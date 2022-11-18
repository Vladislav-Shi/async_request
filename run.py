import argparse
import asyncio
import sys
from datetime import datetime

from app.app import send_combination_request, get_users_chats, create_users_dialog


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--action', default='help')

    return parser


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    print('Start:', datetime.now())
    print(namespace.action)
    if namespace.action == 'get_users_chats':
        asyncio.run(get_users_chats())
    elif namespace.action == 'send_combination_request':
        asyncio.run(send_combination_request())
    elif namespace.action == 'create_users_dialog':
        asyncio.run(create_users_dialog())
    else:
        print('\nДля запуска используйте команду \n"python run.py -a <command>"')
        print('список команд:\n*  send_combination_request -- запускает первоначальный скрипт')
        print('*  create_users_dialog -- создает диалоги')
        print('*  get_users_chats -- запускает подсчет чатов пользователей\n')
    print('End:', datetime.now())
