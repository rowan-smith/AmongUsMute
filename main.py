import os

from discord.ext import commands

import secrets


async def get_prefix_(bot, message):
    return commands.when_mentioned_or("--")(bot, message)


class AmongUs(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=get_prefix_,
            case_insensitive=True
        )

        self.games = {}

        # Working Cogs
        self.load_extension("cogs.new_game_cog")
        self.load_extension("cogs.force_cog")
        self.load_extension("cogs.dead_cog")
        self.load_extension("cogs.emergency_cog")

        # Unchecked
        self.load_extension("cogs.end_game_cog")
        self.load_extension("cogs.reset_cog")
        self.load_extension("cogs.info_cog")

        # Listeners
        self.load_extension("listeners.on_channel_join")

    def run(self):
        try:
            super().run(secrets.TOKEN, reconnect=True)
        finally:
            print("Bot closed.")

    async def on_ready(self):
        print(f'Logged in as {self.user}')


AmongUs().run()
