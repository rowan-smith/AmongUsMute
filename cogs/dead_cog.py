import traceback

from discord import Member
from discord.ext import commands
from discord.ext.commands import Greedy

from main import AmongUs
from utils import is_playing, NoGamesExist, NotPlaying, is_in_voice, VoiceNotConnected
from utils.utils import get_game


async def logic(members, game, ctx):
    dead_count = 0
    for player in members:
        if game.is_alive(player):
            game.add_dead_player(player)
            if game.running:
                await player.edit(mute=False, deafen=False)
            else:
                await player.edit(mute=True)
        else:
            dead_count += 1
            await ctx.send(f"{player.name} is already dead!")

    await ctx.send(f"**{len(members) - dead_count}** player(s) died!")


class Dead(commands.Cog):
    def __init__(self, bot):
        self.bot: AmongUs = bot

    @commands.command()
    @is_playing()
    @is_in_voice()
    async def dead(self, ctx, members: Greedy[Member] = None):

        game = await get_game(self.bot.games, ctx)

        if not game.started:
            return

        if members is None:
            await logic([ctx.author], game, ctx)
        else:
            await logic(members, game, ctx)

    @dead.error
    async def dead_error(self, ctx, error):
        if isinstance(error, NoGamesExist):
            return await ctx.send(error)

        if isinstance(error, (NotPlaying, VoiceNotConnected)):
            return await ctx.send(error)

        traceback.print_exc()


def setup(bot):
    bot.add_cog(Dead(bot))
