from pydantic import BaseModel


class SendParams(BaseModel):
    number: str
    type: str
    message: str
    instance_id: str
    access_token: str


class DialogUser(BaseModel):
    from_user_name: str
    from_user_token: str
    to_user_name: str
    to_user_token: str
