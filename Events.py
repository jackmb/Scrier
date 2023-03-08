# Events.py

import nextcord
import time

from helpers.IntrosHelper import *
from helpers.GenericHelper import *
from helpers.YouTubeHelper import *
from nextcord import User, VoiceState
from nextcord.ext import commands
from dotenv import load_dotenv

load_dotenv()

BOT_ID = int(os.getenv("BOT_ID"))

FFMPEG_EXE = os.getenv("FFMPEG_EXE")

FFMPEG_OPTS = {'executable': FFMPEG_EXE,
               'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
               'options': '-vn'}


class EventCog(commands.Cog):
    """
        nextcord Cog for event handling
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: User, before: VoiceState, after: VoiceState) -> None:
        """
            Event when a user joins a voice channel.
                Plays their intro
        :param member:          The Member joining the voice channel: Member
        :param before:          The VoiceState being left. Not used: VoiceState
        :param after:           The VoiceState being joined: VoiceState
        :return:                None
        """

        # If this voice_state_update isn't a channel being joined, do nothing.
        if type(after.channel) is not nextcord.channel.VoiceChannel:
            return

        # If this voice_state_update is the bot joining a channel, do nothing.
        if member.id == BOT_ID:
            return

        # Connect to the voice channel
        voice_client = await after.channel.connect()

        # Get the user's intro
        url, duration, start_time = get_intro_tuple(member.id)
        url = get_ffmpeg_compatible_link(url)

        # Add option to the FFMPEG command to start at user's start_time and end after user's duration
        ffmpeg_opts = FFMPEG_OPTS
        ffmpeg_opts['before_options'] = ffmpeg_opts['before_options'] + f' -ss {start_time} -t {duration}'

        # Play the user's intro
        voice_client.play(nextcord.FFmpegPCMAudio(url, **FFMPEG_OPTS))

        # Disconnect a third of a second after their intro should end
        time.sleep(float(duration) + 0.33)
        await voice_client.disconnect()

        return

# Load the Events cog
def setup(bot):
    bot.add_cog(EventCog(bot))
    print(f'Loaded EventCog')
