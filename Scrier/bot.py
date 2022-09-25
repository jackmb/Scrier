# musicBot.py

"""
Intro Bot
    Plays YouTube linked videos in discord voice channel when a user joins
    @author: Jack Brashier
"""

import os
import nextcord
import events
import time

from nextcord.ext import commands as disc_commands
from nextcord import Intents
from dotenv import load_dotenv
from utils import ConfigUtil
from cogs import IntroBot
from config import *

Intents.voice_states = True

# Create member vars
config = ConfigUtil()

# Create Bot
load_dotenv()
intents = nextcord.Intents.all()
bot = disc_commands.Bot(command_prefix=config.get_prefix, intents=intents, help_command=None)


@bot.event
async def on_ready():
    """
        Called when bot start-up has finished
    """
    bot.load_extension('events.Events')
    bot.add_cog(IntroBot(bot))


if __name__ == "__main__":
    # Run bot
    bot.run(TOKEN, reconnect=True)
