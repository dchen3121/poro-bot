import discord
import os
from static.constants import *

client = discord.Client()  # client connection to discord

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


# the on_message function triggers each time a message is received
@client.event
async def on_message(message):
    # we don't want to do anything if the message is from ourselves
    if message.author == client.user:
        return

    if message.content.startswith(PREFIX):
        pass  # process the command

    if 'when' in message.content.lower():
        await message.channel.send('Soon')

    if 'im ' in message.content.lower():
        im_index = message.content.lower().find('im ')
        await message.channel.send(f'Hi {message.content[im_index + 3:].strip()}, I\'m Dad!')

client.run(os.getenv('TOKEN'))