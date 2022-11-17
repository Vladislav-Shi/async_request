"""
Данный скрипт содержит все функции для генерации параметров запроса
"""
from v2.app.models import SendParams, SendFileParams
from v2.settings.config import config


def generate_send_params(from_user: str, to_user: str, messages: str) -> SendParams:
    return SendParams(
        number=to_user,
        type='text',
        message=messages,
        instance_id=from_user,
        access_token=config.TOKEN
    )


def generate_send_params_with_file(
        from_user: str,
        to_user: str,
        messages: str,
        file_url: str,
        file_name: str
) -> SendFileParams:
    """Создает набор параметров для отправки файла"""
    return SendFileParams(
        number=to_user,
        type='text',
        message=messages,
        instance_id=from_user,
        access_token=config.TOKEN,
        filename=file_name,
        media_url=file_url
    )