import traceback

from discord import Member
from discord.ext import commands
from discord.ext.commands import Greedy, BotMissingPermissions

from main import AmongUs
from utils import NoGamesExist, NotPlaying, is_playing, is_not_spectator
from utils.exceptions import AlreadySpectating
from utils.utils import get_game


class Spectator(commands.Cog):
    def __init__(self, bot):
        self.bot: AmongUs = bot

    @commands.command(aliases=["spectating"])
    @commands.bot_has_guild_permissions(mute_members=True, deafen_members=True)
    @is_playing()
    @is_not_spectator()
    async def spectator(self, ctx, members: Greedy[Member] = None):

        game = await get_game(self.bot.games, ctx)

        if members:
            for player in members:
                if game.is_spectating(player) or game.is_dead(player):
                    raise AlreadySpectating()
                else:
                    game.add_spectator(player)
                    if game.running:
                        await player.edit(mute=False, deafen=False)
                    else:
                        await player.edit(mute=True, deafen=False)
            await ctx.send(f"**{len(members)}** members added as spectator!!")
        else:
            if game.is_spectating(ctx.author) or game.is_dead(ctx.author):
                raise AlreadySpectating()
            else:
                game.add_spectator(ctx.author)
                if game.running:
                    await ctx.author.edit(mute=False, deafen=False)
                else:
                    await ctx.author.edit(mute=True, deafen=False)
            await ctx.send(f"**{len([ctx.author])}** members added as spectator!!")

    @spectator.error
    async def dead_error(self, ctx, error):
        if isinstance(error, (NoGamesExist, NotPlaying, AlreadySpectating)):
            return await ctx.send(error)

        if isinstance(error, BotMissingPermissions):
            return await ctx.send(error)

        traceback.print_exc()


def setup(bot):
    bot.add_cog(Spectator(bot))
