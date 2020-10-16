import traceback

from discord.ext import commands

from main import AmongUs
from utils.Player import Player
from utils.enum import PlayerState, GameState


class Test(commands.Cog):
    def __init__(self, bot: AmongUs):
        self.bot = bot

    @commands.command(name="test")
    async def test(self, ctx):
        player = Player(ctx.author)
        game = await self.bot.game_handler.get_game(player)

        game.set_game_state(GameState.EMERGENCY)

        player = game.get_player(player)
        player.set_state(PlayerState.DEAD)

        await game.update_message(self.bot)

    @test.error
    async def _new_game_error(self, ctx, error):
        traceback.print_exc()


def setup(bot):
    bot.add_cog(Test(bot))
