"""
Intro Bot
    Plays user-specified Youtube snippets when they join a Discord voice channel
    @author: Jack Brashier
"""

import os
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX")


bot = commands.Bot(command_prefix='$', intents=nextcord.Intents.all(), case_insensitive=True,
                   description='Introduction Bot')
bot.remove_command('help')

# Loop through and load all the cogs in the cogs directory
for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nNextcord Version: {nextcord.__version__}\n')

    await bot.change_presence(activity=nextcord.Game(name='introductions'))
    print(f'IntroBot Loaded\nGuilds:')
    for guild in bot.guilds:
        print(f'\t{guild.name} - {guild.owner.name}')
    print(f'\n--------------------------------------\n')

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot.run(token=TOKEN, reconnect=True)
