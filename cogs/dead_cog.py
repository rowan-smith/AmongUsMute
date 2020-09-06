import traceback

from discord import Member
from discord.ext import commands
from discord.ext.commands import Greedy, BotMissingPermissions

from main import AmongUs
from utils import is_playing, NoGamesExist, NotPlaying
from utils.utils import get_game


class Dead(commands.Cog):
    def __init__(self, bot):
        self.bot: AmongUs = bot

    @commands.command()
    @commands.bot_has_guild_permissions(mute_members=True, deafen_members=True)
    @is_playing()
    async def dead(self, ctx, members: Greedy[Member] = None):

        game = await get_game(self.bot.games, ctx)
        if members is None or not game.started:
            return

        for player in members:
            if game.is_alive(player):
                game.add_dead_player(player)
                if game.status:
                    await player.edit(mute=False, deafen=False)
                else:
                    await player.edit(mute=True)

        await ctx.send(f"{len(members)} died!")

    @dead.error
    async def dead_error(self, ctx, error):
        if isinstance(error, NoGamesExist):
            return await ctx.send(error)

        if isinstance(error, NotPlaying):
            return await ctx.send(error)

        if isinstance(error, BotMissingPermissions):
            return await ctx.send(error)

        traceback.print_exc()


def setup(bot):
    bot.add_cog(Dead(bot))
