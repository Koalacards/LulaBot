from peewee import *

database = SqliteDatabase('botdata.db')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class EmojiData(BaseModel):
    emoji = TextField(null=True)
    message_id = IntegerField(null=True)
    role = TextField(null=True)

    class Meta:
        table_name = 'Emoji'
        primary_key = False

