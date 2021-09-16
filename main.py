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

    if W:
        if any(when_str in message.content.lower() for when_str in {'when ', 'when\'', 'when?'}) or message.content.lower().endswith('when'):
            await message.channel.send('Soon')
        if any(who_str in message.content.lower() for who_str in {'who ', 'who\'', 'whos', 'who?'}) or message.content.lower().endswith('who'):
            await message.channel.send('Me, Poro')

    if PORO_REACT:
        if message.content.lower() == 'good poro':
            await message.channel.send('ଘ(੭ˊᵕˋ)੭ uwu')
        if message.content.lower() == 'bad poro':
            await message.channel.send('(ಥ﹏ಥ)')

    if DAD_JOKES:
        if 'im ' in message.content.lower():
            im_index = message.content.lower().find('im ')
            await message.channel.send(f'Hi {message.content[im_index + 3:].strip()}, I\'m Poro!')
        if 'i\'m ' in message.content.lower():
            im_index = message.content.lower().find('i\'m ')
            await message.channel.send(f'Hi {message.content[im_index + 3:].strip()}, I\'m Poro!')
        if 'i am ' in message.content.lower():
            im_index = message.content.lower().find('i am ')
            await message.channel.send(f'Hi {message.content[im_index + 3:].strip()}, I\'m Poro!')
        if any(fk_off_str in message.content.lower() for fk_off_str in {'fuck off', 'fk off', 'fuck right off', 'fck off'}):
            await message.channel.send('Who\'s off (゜。゜)?')

    await bot.process_commands(message)

# @bot.command(name='sayhi')
# async def say_hi(ctx):
#     await ctx.send(f'Hi @{ctx.message.author.name}')

bot.add_cog(Music(bot))

bot.run(TOKEN)
