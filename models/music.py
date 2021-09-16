from discord.ext import commands
from models.ytdl import YTDLSource
from collections import deque

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song_queue = deque()
        self.player = None
        self.url = None

    def play_next(self, ctx):
        if self.song_queue:
            player, url = self.song_queue.popleft()
            self.player = player
            self.url = url
            # async with ctx.typing():
            #     await ctx.send(f'Now playing: {player.title}\n{url}')
            ctx.voice_client.play(player, after=lambda e: self.play_next(ctx))
        else:
            self.player = None
            self.url = None

    @commands.command(aliases=['p', 'stream', 'yt'])
    async def play(self, ctx, *, search_keyword):
        """Streams from a youtube link"""
        async with ctx.typing():
            player, url = await YTDLSource.search(search_keyword, loop=self.bot.loop, stream=True)

        if ctx.voice_client.is_playing() or self.song_queue:
            await ctx.send(f'{ctx.message.author.mention} Added song to back of current playing queue: {player.title}')
            self.song_queue.append((player, url))
        else:
            self.player = player
            self.url = url
            async with ctx.typing():
                await ctx.send(f'{ctx.message.author.mention} Now playing: {player.title}\n{url}')

            ctx.voice_client.play(player, after=lambda e: self.play_next(ctx))

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
        if ctx.voice_client.is_connected():
            await ctx.voice_client.disconnect()

    @commands.command(aliases=['nowplaying'])
    async def now_playing(self, ctx):
        """Shows the song and url currently playing"""
        if ctx.voice_client.is_connected() and ctx.voice_client.is_playing() and self.player.title and self.url:
            await ctx.send(f'Now playing: {self.player.title}\n{self.url}')

    @commands.command(aliases=['q'])
    async def queue(self, ctx):
        """Shows the current playing queue"""
        if ctx.voice_client.is_connected() and ctx.voice_client.is_playing():
            msg = f'Now playing: {self.player.title}\n{self.url}\n'
            if self.song_queue:
                for i, song in enumerate(self.song_queue):
                    player, _ = song
                    msg += f'{i + 1}: {player.title}\n'
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
