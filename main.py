import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

from static.constants import *
from models.music import Music


load_dotenv()
TOKEN = os.getenv('TOKEN')


bot = commands.Bot(command_prefix=PREFIX)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


# the on_message function triggers each time a message is received
@bot.event
async def on_message(message):
    # we don't want to do anything if the message is from ourselves
    if message.author == bot.user:
        return

    if 'when' in message.content.lower():
        await message.channel.send('Soon')

    if 'im ' in message.content.lower():
        im_index = message.content.lower().find('im ')
        await message.channel.send(f'Hi {message.content[im_index + 3:].strip()}, I\'m Dad!')

    await bot.process_commands(message)

@bot.command(name='sayhi')
async def say_hi(ctx):
    await ctx.send(f'Hi @{ctx.message.author.name}')

bot.add_cog(Music(bot))

bot.run(TOKEN)
