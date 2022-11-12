import dataclasses

from dotenv import dotenv_values


@dataclasses.dataclass
class Config:
    URL: str
    TOKEN: str
    TEXT: str
    LIMIT: int
    OUTPUT: str


config = dotenv_values("settings/.env")
config['LIMIT'] = int(config['LIMIT'])
config = Config(**config)


def get_access_url() -> str:
    return f"{config.URL}/api/get_instance.php"


def get_send_url() -> str:
    return f"{config.TOKEN}/api/send.php"
