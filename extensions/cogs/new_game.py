import traceback

from discord import Message, Embed
from discord.ext import commands

from main import AmongUs


class NewGame(commands.Cog):
    def __init__(self, bot: AmongUs):
        self.bot = bot

    @commands.command(name="new")
    async def _new_game(self, ctx):
        embed = Embed(description="Creating Game... Please Wait.")
        message: Message = await ctx.send(embed=embed)
        game = await self.bot.game_handler.create_game(ctx, message)
        await game.update_message(self.bot)

    @_new_game.error
    async def _new_game_error(self, ctx, error):
        traceback.print_exc()


def setup(bot):
    bot.add_cog(NewGame(bot))
