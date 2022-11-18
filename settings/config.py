from pathlib import Path

import dotenv
from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Config(BaseSettings):
    URL: str
    TOKEN: str
    LOGIN: str
    PASSWORD: str

    TEXT: str = '{hi|Привет|здорова|здарова|приветствую|салам|хай|хаюшки|добрый вечер}'
    LIMIT: int = 1000

    OUTPUT: str = 'output.txt'

    MIN_DIALOG_SIZE: int = 5
    MAX_DIALOG_SIZE: int = 10
    IMAGE_MESSAGE_CHANCE: int = 20

    class Config:
        env_file = Path(BASE_DIR, 'settings', '.env')
        dotenv.load_dotenv(env_file)

    def get_access_url(self) -> str:
        return f"{self.URL}/api/get_instance.php"

    def get_send_url(self) -> str:
        return f"{self.URL}/api/send.php"

    def get_file_manager_url(self) -> str:
        return f'{self.URL}/file_manager/ajax_load//all'

    def get_login_url(self) -> str:
        return f'{self.URL}/wimax/ajax_login'

    def get_chat_url(self) -> str:
        return f'{self.URL}/whatsapp/get/chat'


config = Config()

TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": ["app.database", "aerich.models"],
            "default_connection": "default",
        },
    },
}