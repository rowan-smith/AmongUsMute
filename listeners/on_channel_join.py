from discord.ext import commands

from main import AmongUs


class OnJoinListener(commands.Cog):
    def __init__(self, bot):
        self.bot: AmongUs = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if before.channel is None:
            await member.edit(mute=False, deafen=False)
            for game in self.bot.games:
                if game.is_channel(after.channel):
                    if game.is_playing(member):
                        if game.is_alive(member):
                            if game.status:
                                await member.edit(deafen=True)
                            else:
                                await member.edit(deafen=False, mute=False)
                        else:
                            if game.status:
                                await member.edit(mute=False, deafen=False)
                            else:
                                await member.edit(mute=True)
                    else:
                        if game.started:
                            if game.status:
                                await member.edit(mute=False, deafen=False)
                            else:
                                await member.edit(mute=True)
                            if member not in game.spectating_players:
                                game.add_spectator(member)
                        else:
                            game.add_player(member)


def setup(bot):
    bot.add_cog(OnJoinListener(bot))
