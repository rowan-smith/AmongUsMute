import traceback

from discord import Member
from discord.ext import commands
from discord.ext.commands import Greedy, BotMissingPermissions

from main import AmongUs
from utils import NoGamesExist, NotPlaying, is_not_playing
from utils.exceptions import AlreadySpectating
from utils.utils import get_game


class Spectator(commands.Cog):
    def __init__(self, bot):
        self.bot: AmongUs = bot

    @commands.command()
    @commands.bot_has_guild_permissions(mute_members=True, deafen_members=True)
    @is_not_playing()
    async def spectator(self, ctx, members: Greedy[Member] = None):

        game = await get_game(self.bot.games, ctx)

        for player in members:
            if game.is_spectating(player):
                raise AlreadySpectating()
            else:
                game.add_spectator(player)
                if game.status:
                    await player.edit(mute=False)
                else:
                    await player.edit(mute=True)

        await ctx.send(f"{len(members)} members added as spectator!!")

    @spectator.error
    async def dead_error(self, ctx, error):
        if isinstance(error, (NoGamesExist, NotPlaying, BotMissingPermissions, AlreadySpectating)):
            return await ctx.send(error)

        traceback.print_exc()


def setup(bot):
    bot.add_cog(Spectator(bot))
