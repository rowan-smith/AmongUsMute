import traceback

from discord.ext import commands
from discord.ext.commands import Context

from main import AmongUs
from utils import is_in_voice, VoiceNotConnected, NotPlaying, NoGamesExist
from utils.utils import get_game


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot: AmongUs = bot

    @commands.command()
    @is_in_voice()
    async def info(self, ctx: Context):
        game = await get_game(self.bot.games, ctx)

        await ctx.send(f"Alive: {len(game.players)},\n"
                       f"Dead: {len(game.dead_players)},\n"
                       f"Spectating: {len(game.spectating_players)},\n"
                       f"Game Started: {game.started},\n"
                       f"Status: {game.status}")

    @info.error
    async def info_error(self, ctx, error):
        if isinstance(error, VoiceNotConnected):
            return await ctx.send(error)

        if isinstance(error, NotPlaying):
            return await ctx.send(error)

        if isinstance(error, NoGamesExist):
            return await ctx.send(error)

        traceback.print_exc()


def setup(bot):
    bot.add_cog(Info(bot))
