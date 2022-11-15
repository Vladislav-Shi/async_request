from pydantic import BaseModel


class SendParams(BaseModel):
    number: str
    type: str
    message: str
    instance_id: str
    access_token: str


class DialogUser(BaseModel):
    from_user: str
    to_user: str
