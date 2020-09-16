import traceback

from discord.ext import commands

from main import AmongUs
from utils import is_in_voice, VoiceNotConnected, is_not_playing, AlreadyPlaying
from utils.utils import create_game


class EndGame(commands.Cog):
    def __init__(self, bot):
        self.bot: AmongUs = bot

    @commands.command(name="newgame")
    @is_in_voice()
    @is_not_playing()
    async def new_game(self, ctx):
        game = await create_game(self.bot.games, ctx)
        await ctx.send(f"Created game with **{len(game.players)}** members")

    @new_game.error
    async def end_game_error(self, ctx, error):
        if isinstance(error, VoiceNotConnected):
            return await ctx.send(error)

        if isinstance(error, AlreadyPlaying):
            return await ctx.send(error)

        traceback.print_exc()


def setup(bot):
    bot.add_cog(EndGame(bot))
