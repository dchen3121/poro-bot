from discord.ext import commands
from models.ytdl import YTDLSource
from collections import deque
from static.constants import SONG_QUEUES

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def play_next(self, ctx, guild_id=None):
        if not guild_id:
            guild_id = ctx.guild.id
        if guild_id not in SONG_QUEUES:
            SONG_QUEUES[guild_id] = deque()

        song_queue = SONG_QUEUES[guild_id]
        song_queue.popleft()
        if song_queue:
            player, url = song_queue[0]
            # async with ctx.typing():
            #     await ctx.send(f'Now playing: {player.title}\n{url}')
            ctx.voice_client.play(player, after=lambda e: self.play_next(ctx, guild_id))

    @commands.command(aliases=['p', 'stream', 'yt'])
    async def play(self, ctx, *, search_keyword):
        """Streams from a youtube link"""
        async with ctx.typing():
            player, url = await YTDLSource.search(search_keyword, loop=self.bot.loop, stream=True)

        if ctx.guild.id not in SONG_QUEUES:
            SONG_QUEUES[ctx.guild.id] = deque()
        SONG_QUEUES[ctx.guild.id].append((player, url))

        if ctx.voice_client.is_playing():
            await ctx.send(f'{ctx.message.author.mention} Added song to back of current playing queue: {player.title}')
        else:
            async with ctx.typing():
                ctx.voice_client.play(player, after=lambda e: self.play_next(ctx))
                await ctx.send(f'{ctx.message.author.mention} Now playing: {player.title}\n{url}')

    @commands.command(help='Pauses the current audio playing')
    async def pause(self, ctx):
        """Pauses the current audio playing"""
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
        else:
            await ctx.send(f'Poro is not playing anything at the moment :thinking:')

    @commands.command(help='Resumes the current audio playing')
    async def resume(self, ctx):
        """Resumes the current audio playing"""
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
        else:
            await ctx.send(f'Nothing is paused at the moment :thinking:')

    @commands.command(help='Skip the current song or the n-th song in queue')
    async def skip(self, ctx, *, skip_index=0):
        """Skips the current song from voice"""
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    @commands.command(aliases=['dc', 'disconnect'])
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        SONG_QUEUES[ctx.guild.id] = deque()
        await ctx.voice_client.disconnect()

    @commands.command(aliases=['nowplaying', 'np'])
    async def now_playing(self, ctx):
        """Shows the song and url currently playing"""
        if ctx.voice_client.is_connected() and ctx.voice_client.is_playing():
            player, url = SONG_QUEUES[ctx.guild.id][0]
            await ctx.send(f'Now playing: {player.title}\n{url}')

    @commands.command(aliases=['q'])
    async def queue(self, ctx):
        """Shows the current playing queue"""
        if ctx.voice_client.is_connected() and ctx.voice_client.is_playing():
            song_queue = SONG_QUEUES[ctx.guild.id]
            msg = ''
            if song_queue:
                for i, song in enumerate(song_queue):
                    player, _ = song
                    msg += f'{i + 1}: {player.title}\n'
            if msg:
                await ctx.send(msg)

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel :frowning:")
                raise commands.CommandError("Author not connected to a voice channel.")

    @pause.before_invoke
    @resume.before_invoke
    @stop.before_invoke
    @skip.before_invoke
    @now_playing.before_invoke
    async def check_voice(self, ctx):
        if not ctx.author.voice:
            await ctx.send('You are not connected to a voice channel :frowning:')
            raise commands.CommandError("Author not connected to a voice channel.")
        if ctx.voice_client is None:
            raise commands.CommandError("Poro bot not connected to a voice channel.")
