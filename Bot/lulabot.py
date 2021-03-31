import discord
from discord.ext import commands
from confidential import *
import luladbfunctions

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

role_emoji_pairs = {}

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="meow"))
    print("meow")


@client.command()
async def add_emoji_role_pair(ctx, role_emoji:str, *, role_name:str):
    global role_emoji_pairs
    try:
        await ctx.message.add_reaction(role_emoji)
    except:
        await ctx.send("emoji cannot be used by bot")
        return

    guild = ctx.guild
    role = discord.utils.get(guild.roles, name=role_name)
    if role is None:
        await guild.create_role(name=role_name)

    role_emoji_pairs[role_name] = role_emoji
    await ctx.send(":thumbsup:")


@client.command()
async def create_role_message(ctx, channel_name:str):
    global role_emoji_pairs
    guild = ctx.guild
    channel = discord.utils.get(guild.channels, name=channel_name)
    if channel is None:
        await ctx.send("no channel exists with that name")
        return
    elif len(role_emoji_pairs.keys()) == 0:
        await ctx.send("there are no role emoji pairs")
        return
    else:
        description_text= "**React with the appropriate emoji to get the appropriate role:**\n\n"
        for role, emoji in role_emoji_pairs.items():
            description_text = description_text + f'\n{emoji} - {role}'


        embed = discord.Embed(
            title="Emoji Selector!",
            description=description_text,
            colour= discord.Color.green()
        )

    message = await channel.send(embed=embed)
    luladbfunctions.add_items(message.id, role_emoji_pairs)
    role_emoji_pairs = {}

@client.event
async def on_raw_reaction_add(payload):
    channel = await client.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    guild = message.guild
    emoji = payload.emoji
    user = payload.member
    list_from_db = luladbfunctions.get_row_with_message_and_emoji(payload.message_id, str(emoji))
    role_name = ''
    if len(list_from_db) == 1:
        for row in list_from_db:
            role_name = row.role
    else:
        return
    
    role = discord.utils.get(guild.roles, name=role_name)
    if role is None:
        return
    else:
        await user.add_roles(role)


@client.event
async def on_raw_reaction_remove(payload):
    channel = await client.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    guild = message.guild
    emoji = payload.emoji
    user = guild.get_member(payload.user_id)
    list_from_db = luladbfunctions.get_row_with_message_and_emoji(payload.message_id, str(emoji))
    role_name = ''
    if len(list_from_db) == 1:
        for row in list_from_db:
            role_name = row.role
    else:
        return
    
    role = discord.utils.get(guild.roles, name=role_name)
    if role is None:
        return
    else:
        await user.remove_roles(role)
        
    

client.run(RUN_ID)