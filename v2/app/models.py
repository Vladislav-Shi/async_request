from pydantic import BaseModel


class UserInstance(BaseModel):
    created: str
    name: str
    pid: str
    sent: int
    token: str
    username: str


class SendParams(BaseModel):
    number: str
    message: str
    instance_id: str
    access_token: str
    type: str = 'text'


class SendFileParams(SendParams):
    filename: str
    media_url: str


class DialogUser(BaseModel):
    type: str = 'media'
    from_user_name: str
    from_user_token: str
    to_user_name: str
    to_user_token: str
