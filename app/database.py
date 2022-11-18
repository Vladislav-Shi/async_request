from tortoise.models import Model
from tortoise import fields


class Dialogs(Model):
    id = fields.IntField(pk=True)
    user1 = fields.CharField(max_length=32)
    user2 = fields.CharField(max_length=32)
