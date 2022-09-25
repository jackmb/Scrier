# events.py

import time

from cogs import *


class Events(commands.Cog):
    """
    nextcord Cog for event handling
    """

    def __init__(self, bot_e):
        self.bot = bot_e
        self.default_prefix = "$"
        self.utilities = Util()
        self.config_obj = ConfigUtil()
        self.command_cog = bot_e.get_cog("Commands")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """
            Removes guild id and stored prefix from config.ini
        :param guild:   nextcord.Guild object, automatically passed
        :return:        None
        """
        # Set prefix of new server to default prefix and loop toggle
        default = {"prefix": self.default_prefix, "loop": False}
        self.config_obj.write_config('w', "SERVER_SETTINGS", str(guild.id), default)

        # Update server queues
        self.command_cog.queues.create_server_queue()

        print(f"{self.bot.user.name} added to {guild.name}!")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """
            Removes guild id and stored prefix from config.ini
        :param guild:   nextcord.Guild object, automatically passed
        :return:        None
        """
        # remove server's prefix from config
        self.config_obj.write_config('d', "SERVER_SETTINGS", str(guild.id))

        print(f"{self.bot.user.name} removed from {guild.name}")
