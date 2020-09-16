import asyncio
import traceback

from discord.ext import commands
from discord.ext.commands import CommandOnCooldown, BucketType, BotMissingPermissions

from main import AmongUs
from utils import is_playing, NotPlaying, AlreadyPlaying, VoiceNotConnected, is_in_voice
from utils.utils import get_game, resume_game, pause_game


class Emergency(commands.Cog):
    def __init__(self, bot):
        self.bot: AmongUs = bot

    @commands.command(aliases=["em", "emergency", "report", "re", "start"])
    @commands.bot_has_guild_permissions(mute_members=True, deafen_members=True)
    @commands.cooldown(1, 10, BucketType.channel)
    @is_in_voice()
    @is_playing()
    async def _emergency(self, ctx):
        """Command for when an emergency or report has happened."""
        game = await get_game(self.bot.games, ctx)

        if not game.started:
            game.started = True
        game.running = not game.running

        if game.running:
            await pause_game(game, ctx)
        else:
            await resume_game(game, ctx)

        def check(m):
            return game.is_playing(m.author)

        try:
            await self.bot.wait_for('message', check=check, timeout=600)
        except asyncio.TimeoutError:
            await self.bot.games.remove(game)
            await ctx.send("Game has been idle for too long an ended.")

    @_emergency.error
    async def emergency_error(self, ctx, error):
        if isinstance(error, VoiceNotConnected):
            return await ctx.send(error)

        if isinstance(error, (NotPlaying, AlreadyPlaying)):
            return await ctx.send(error)

        if isinstance(error, (BotMissingPermissions, CommandOnCooldown)):
            return await ctx.send(error)

        traceback.print_exc()


def setup(bot):
    bot.add_cog(Emergency(bot))
