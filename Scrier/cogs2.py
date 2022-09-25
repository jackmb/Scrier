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
        return

    @commands.command()
    async def set(self, ctx, *, url):
        """Downloads and saves a user's intro"""
        add_intro(ctx, url)
        return

    @commands.command()
    async def get(self, ctx):
        """Puts a user's intro in the chat"""
        return

    @commands.command()
    async def clear(self, ctx):
        """Deletes a user's intro"""
        return

    @commands.command()
    async def test(self, ctx):
        """Types a test command in the chat"""
        await ctx.send(str(ctx.author) + " test command")

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        await ctx.voice_client.disconnect()

    @commands.Cog.listener()
    async def on_voice_state_update(self, ctx, before, after):
        print("VOICE STATE UPDATE")
        """
            Joins a channel when a user with an intro does.
        :param member:  nextcord Member object of member whose voice state changed, automatically passed
        :param before:  nextcord VoiceState prior to change, automatically passed
        :param after:   nextcord VoiceState after change, automatically passed
        :return:        None
        """
        if ctx == 'WhosThat#7220':
            return

        print(ctx, type(ctx))
        if joining_from_none(before, after) and has_intro(ctx.id):
            time.sleep(0.1)
            await IntroBot.stream(self, ctx)

            print(f'Introducing {ctx.name} in {ctx.guild}')

    @play.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


bot = commands.Bot(command_prefix="$")


bot.add_cog(IntroBot(bot))
bot.run(config.TOKEN)
