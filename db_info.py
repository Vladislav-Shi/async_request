import argparse
import asyncio
import sys

from tortoise.expressions import Q

from app.app import init_bd
from app.database import Dialogs


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', default='000000000')

    return parser


async def main():
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    await init_bd()
    dialogs = await Dialogs.all().count()
    print('Всего диалогов в бд:', dialogs)

    print(f'Диалогов пользователя {namespace.number}:', end=' ')
    dialogs = await Dialogs.filter(
        Q(user1=namespace.number) | Q(user2=namespace.number)
    )
    print(len(dialogs))


asyncio.run(main())
