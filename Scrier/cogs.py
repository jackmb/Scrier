import config
import time
from nextcord.ext import commands
from utils import *

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'cookiefile': 'cookies.txt',
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'executable': 'C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(nextcord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(nextcord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class IntroBot(commands.Cog):
    def __init__(self, bot_v):
        self.bot = bot_v

    @commands.command()
    async def invite(self, ctx):
        try:
            await ctx.message.delete(delay=15)
        except nextcord.DiscordException:
            pass

        await ctx.send(f'Invite IntroBot to your server with\n{config.INVITE_LINK}')

    @commands.command()
    async def join(self, ctx, *, channel: nextcord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    # DEPRECATE
    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        initialize_pickle()

        source = nextcord.PCMVolumeTransformer(nextcord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {query}')

    @commands.command()
    async def stream(self, ctx, user=None):
        """Streams from a url"""

        try:
            auth = ctx.author
        except AttributeError:
            auth = ctx

        initialize_pickle()

        if ctx is not None and user is None:
            user = auth.id

        if has_intro(user):
            url = get_intro(user)
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            vc = await ctx.voice.channel.connect()
            vc.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
            while vc.is_playing():
                time.sleep(0.5)
            await vc.disconnect()
        else:
            print(f'{auth} joined a channel but does not have an intro')

    @commands.command()
    async def set(self, ctx, *, url):
        """Stores a user's desired intro"""

        initialize_pickle()

        async with ctx.typing():
            add_intro(ctx.author, url)

        await ctx.send(f'{ctx.author}\'s intro saved')

    @commands.command()
    async def get(self, ctx):
        try:
            await ctx.send(f'{str(ctx.author)}\'s Intro: {get_intro(ctx.author.id)}')
        except nextcord.DiscordException:
            pass
        except KeyError:
            await ctx.send(f'{str(ctx.author)} does not have an intro set')

    @commands.command()
    async def clear(self, ctx):
        """Deletes a user's intro"""

        # if pickle didn't exist, make it and return.
        if initialize_pickle():
            return

        async with ctx.typing():
            try:
                remove_intro(ctx.author.id)
            except EOFError:
                print(ctx.author.id + " tried to clear an intro they didn't have")

            await ctx.send(f'{ctx.author}\'s intro cleared')

    # WIP
    @commands.command()
    async def test(self, ctx):
        """Test"""

        await ctx.send(str(ctx.author) + " test command")

    # DONE
    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    # DONE
    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        await ctx.voice_client.disconnect()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """
            Joins a channel when a user with an intro does.
        :param member:  nextcord Member object of member whose voice state changed, automatically passed
        :param before:  nextcord VoiceState prior to change, automatically passed
        :param after:   nextcord VoiceState after change, automatically passed
        :return:        None
        """
        if member == 'WhosThat#7220':
            return

        if (before.channel is None) and (has_intro(member.id)):
            await IntroBot.play(self, member)

            print(f'Introducing {member.name} in {member.guild}')


bot = commands.Bot(command_prefix="$")


bot.add_cog(IntroBot(bot))
bot.run(config.TOKEN)
