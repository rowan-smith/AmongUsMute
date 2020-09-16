import traceback

from discord.ext import commands

from main import AmongUs
from utils import is_playing, is_in_voice, NotPlaying, NoGamesExist
from utils.utils import get_game, end_game


class EndGame(commands.Cog):
    def __init__(self, bot):
        self.bot: AmongUs = bot

    @commands.command(name="endgame")
    @is_playing()
    async def end_game(self, ctx):
        game = await get_game(self.bot.games, ctx)
        await end_game(game)
        self.bot.games.remove(game)
        await ctx.send(f"The game has ended in channel **{game.channel.name}**")

    @end_game.error
    async def end_game_error(self, ctx, error):
        if isinstance(error, (NotPlaying, NoGamesExist)):
            return ctx.send(error)

        traceback.print_exc()
            

def setup(bot):
    bot.add_cog(EndGame(bot))
