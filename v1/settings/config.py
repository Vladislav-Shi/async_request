from pathlib import Path

import dotenv
from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Config(BaseSettings):
    URL: str
    TOKEN: str

    TEXT: str = '{hi|Привет|здорова|здарова|приветствую|салам|хай|хаюшки|добрый вечер}'
    LIMIT: int = 1000

    OUTPUT: str = 'output.txt'

    MIN_DIALOG_SIZE: int = 5
    MAX_DIALOG_SIZE: int = 10

    class Config:
        env_file = Path(BASE_DIR, 'settings', '.env')
        dotenv.load_dotenv(env_file)


config = Config()


def get_access_url() -> str:
    return f"{config.URL}/api/get_instance.php"


def get_send_url() -> str:
    return f"{config.URL}/api/send.php"
