import discord
from peewee import *
from lulamodels import *

def add_items(message_id:int, roles_dict):
    for role, emoji in roles_dict.items():
        EmojiData.create(message_id=message_id, role=role, emoji=str(emoji))

def get_row_with_message_and_emoji(message_id:int, emoji:str):
    return EmojiData.select().where(EmojiData.message_id == message_id and EmojiData.emoji == emoji)