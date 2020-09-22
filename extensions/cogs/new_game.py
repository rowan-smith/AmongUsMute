import traceback

from discord.ext import commands

from main import AmongUs


class NewGame(commands.Cog):
    def __init__(self, bot: AmongUs):
        self.bot = bot

    @commands.command(name="new")
    async def _new_game(self, ctx):
        game = await self.bot.game_handler.create_game(ctx)

        for member in game.voice_channel.members:
            await game.new_player(member)

        if game:
            await ctx.send(f"Created game with **{await game.get_player_count()}** members in **{game.voice_channel.name}**")

    @_new_game.error
    async def _new_game_error(self, ctx, error):
        traceback.print_exc()


def setup(bot):
    bot.add_cog(NewGame(bot))
