from discord.ext import commands
from discord.ext.commands import CommandInvokeError

from main import AmongUs
from utils import is_playing
from utils.utils import get_game


class EndGame(commands.Cog):
    def __init__(self, bot):
        self.bot: AmongUs = bot

    @commands.command(name="endgame")
    @is_playing()
    async def end_game(self, ctx):

        game = await get_game(self.bot.games, ctx)

        if not len(game.players) <= 3:
            return await ctx.send("Cannot end game with more than 3 players.")

        for player in game.players:
            await player.edit(mute=False, deafen=False)
        for player in game.dead_players:
            await player.edit(mute=False, deafen=False)
        for player in game.spectating_players:
            await player.edit(mute=False, deafen=False)

        self.bot.games.remove(game)

        await ctx.send("Game has ended.")

    @end_game.error
    async def end_game_error(self, ctx, error):
        if isinstance(error, CommandInvokeError):
            return
            

def setup(bot):
    bot.add_cog(EndGame(bot))
