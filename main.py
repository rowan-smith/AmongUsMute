from discord.ext import commands

import secrets


async def get_prefix_(bot, message):
    return commands.when_mentioned_or(*["--", "—"])(bot, message)


class AmongUs(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=get_prefix_,
            case_insensitive=True
        )

        self.load_extension("cogs.react")

    def run(self):
        try:
            super().run(secrets.TOKEN, reconnect=True)
        finally:
            print("Bot closed.")

    async def on_ready(self):
        print(f'Logged in as {self.user}')


AmongUs().run()
