import discord
from discord.ext import commands
from models.ytdl import YTDLSource

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['p', 'stream', 'yt'])
    async def play(self, ctx, *, search_keyword):
        """Streams from a youtube link"""

        async with ctx.typing():
            player, url = await YTDLSource.search(search_keyword, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'{ctx.message.author.mention} Now playing: {player.title}\n{url}')

    @commands.command(aliases=['vol'])
    async def volume(self, ctx, volume: int):
        """Changes the player's volume (0-100)"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
