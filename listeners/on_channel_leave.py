from discord.ext import commands

from main import AmongUs


class OnLeaveListener(commands.Cog):
    def __init__(self, bot):
        self.bot: AmongUs = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if after.channel is None:
            for game in self.bot.games:
                if game.is_channel(after.channel):
                    if game.is_playing(member):
                        if not game.started:
                            try:
                                game.players.remove(member)
                            except Exception:
                                pass
                            try:
                                game.dead_players.remove(member)
                            except Exception:
                                pass


def setup(bot):
    bot.add_cog(OnLeaveListener(bot))
