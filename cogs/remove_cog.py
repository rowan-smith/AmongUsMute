import traceback

from discord import Member
from discord.ext import commands
from discord.ext.commands import Greedy

from main import AmongUs
from utils import VoiceNotConnected, AlreadyPlaying, is_playing, NotPlaying
from utils.utils import create_game


class Remove(commands.Cog):
    def __init__(self, bot):
        self.bot: AmongUs = bot

    @commands.command(name="remove")
    @is_playing()
    async def new_game(self, ctx, members: Greedy[Member] = None):
        game = await create_game(self.bot.games, ctx)

        fail_count = 0
        for i in members:
            try:
                game.players.remove(i)
            except ValueError:
                fail_count += 1

            try:
                game.dead_players.remove(i)
            except ValueError:
                fail_count += 1

        await ctx.send(f"{len(members) - fail_count} members have been removed")

    @new_game.error
    async def end_game_error(self, ctx, error):
        if isinstance(error, VoiceNotConnected):
            return await ctx.send(error)

        if isinstance(error, (AlreadyPlaying, NotPlaying)):
            return await ctx.send(error)

        traceback.print_exc()


def setup(bot):
    bot.add_cog(Remove(bot))
