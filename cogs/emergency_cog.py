import asyncio
import traceback

from discord.ext import commands
from discord.ext.commands import CommandOnCooldown, BucketType, BotMissingPermissions

from main import AmongUs
from utils import is_playing, NoGamesExist, NotPlaying
from utils.utils import get_game


class Emergency(commands.Cog):
    def __init__(self, bot):
        self.bot: AmongUs = bot

    @commands.command(aliases=["unmute", "mute", "em", "report", "re", "start"])
    @commands.bot_has_guild_permissions(mute_members=True, deafen_members=True)
    @commands.cooldown(1, 10, BucketType.channel)
    @is_playing()
    async def emergency(self, ctx):
        """Command for when an emergency or report has happened."""

        game = await get_game(self.bot.games, ctx)
        game.started = True

        if game.status:
            for player in game.players:
                await player.edit(deafen=True)

            for player in game.dead_players:
                await player.edit(mute=False)

            for player in game.spectating_players:
                await player.edit(mute=False)

            await ctx.send(f"**{len(game.players)}** Living players have been deafened.\n"
                           f"**{len(game.dead_players) + len(game.spectating_players)}"
                           f"** Dead / Spectating players unmuted.")

            game.status = not game.status

        else:
            for player in game.dead_players:
                await player.edit(mute=True)

            for player in game.spectating_players:
                await player.edit(mute=True)

            for player in game.players:
                await player.edit(deafen=False)

            await ctx.send(f"**{len(game.players)}** players have been undeafened.\n"
                           f"**{len(game.dead_players) + len(game.spectating_players)}"
                           f"** Dead / Spectators players muted.")

        game.status = not game.status

        def check(m):
            return game.is_playing(m.author)

        try:
            await self.bot.wait_for('message', check=check, timeout=600)
        except asyncio.TimeoutError:
            await self.bot.games.remove(game)
            await ctx.send("Game has been idle for too long an ended.")

    @emergency.error
    async def emergency_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            return await ctx.send(error)

        if isinstance(error, NoGamesExist):
            return await ctx.send(error)

        if isinstance(error, NotPlaying):
            return await ctx.send(error)

        if isinstance(error, BotMissingPermissions):
            return await ctx.send(error)

        traceback.print_exc()


def setup(bot):
    bot.add_cog(Emergency(bot))
