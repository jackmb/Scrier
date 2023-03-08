# Commands.py

import asyncio
import nextcord

from helpers.IntrosHelper import *
from helpers.YouTubeHelper import *
from helpers.GenericHelper import *
from helpers.EmbedHelper import *
from nextcord.ext import commands
from nextcord.ext.commands import Context
from dotenv import load_dotenv

load_dotenv()

BOT_ID = int(os.getenv("BOT_ID"))


class CommandCog(commands.Cog):
    """
        nextcord Cog for command handling
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='set', aliases=['setintro', 'set_intro', 'introset', 'intro_set'])
    async def set_(self, ctx: Context, *, arg: str):
        """
            Command to set a user's introduction info
                Stores YouTube link, YouTube video start time, and intro duration
        :param ctx:             Command context: Context
        :param arg:             YouTube video link OR search string: str
        :return:                None
        """

        log_command('set', ctx)

        # If the user tried to do a command in a guild, send them a DM with Scrier info
        if 'Direct Message' not in str(ctx.channel):
            embed = get_dm_info_embed(self.bot, ctx.author)
            await ctx.author.send(embed=embed)
            return

        # If the user tried to do this command without an argument, tell them that's not going to work
        if not arg:
            await ctx.send('You need to specify a URL or search term to set an intro')

        # If the user input a YouTube link, great! Otherwise, resolve their search query to a link.
        url, from_search = get_valid_yt_url(arg)

        # If the user didn't specify their exact video and we found it for them, show them.
        if from_search:
            await ctx.send(url)

        # Responses to the start_time and duration prompts should be in format 'sssss.ms' or 'hh:mm:ss.ms'
        def check(msg: nextcord.Message):
            if msg.author != ctx.message.author:
                return False
            return time_str_to_raw_seconds(msg.content) is not None

        # Get the time in the YouTube video the intro should start
        await ctx.send('Where in the video should your intro begin?')
        try:
            response = await self.bot.wait_for('message', check=check, timeout=60)
        except asyncio.TimeoutError:
            await ctx.send('Your set command timed out')
            return

        start_time = time_str_to_raw_seconds(response.content)

        # Get the duration the YouTube video should play
        await ctx.send('How long should your intro last?')
        try:
            response = await self.bot.wait_for('message', check=check, timeout=60)
        except asyncio.TimeoutError:
            await ctx.send('Your set command timed out')
            return

        duration = time_str_to_raw_seconds(response.content)

        # Save the info we've collected to their respective pickled dictionaries
        set_intro(ctx.message.author.id, url, duration, start_time)

        # Notify the user we've saved their info
        await ctx.send(f'Intro set to {duration} seconds beginning at '
                       f'{start_time} in {get_timestamped_link(url, start_time)}')
        return

    @commands.command(name='get', aliases=['getintro', 'get_intro', 'introget', 'intro_get'])
    async def get_(self, ctx) -> None:
        """
            Command to retrieve a user's introduction info.
                Including YouTube link, start time, and duration.
        :param ctx:             Command context: Context
        :return:                None
        """

        log_command('get', ctx)

        # If the user tried to do a command in a guild, send them a DM with Scrier info
        if 'Direct Message' not in str(ctx.channel):
            embed = get_dm_info_embed(self.bot, ctx.author)
            await ctx.author.send(embed)
            return

        # Using the user ID, retrieve their intro info from the pickled dictionaries
        url, duration, start_time = get_intro_tuple(ctx.message.author.id)

        # Format their intro info nicely
        url = get_timestamped_link(url, start_time)
        duration = raw_seconds_to_time_str(int(duration))
        start_time = raw_seconds_to_time_str(int(start_time))

        # Show the intro info to the user
        await ctx.send(f'Your intro is set to the {duration} seconds beginning at time {start_time} '
                       f'in {url}')
        return

# Load the Commands cog
def setup(bot):
    bot.add_cog(CommandCog(bot))
    print(f'Loaded CommandCog')
