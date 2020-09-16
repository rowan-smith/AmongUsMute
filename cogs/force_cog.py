import traceback

from discord import VoiceState
from discord.ext import commands
from discord.ext.commands import BotMissingPermissions, MissingPermissions, BucketType, CommandInvokeError

from main import AmongUs
from utils import is_in_voice, VoiceNotConnected, is_playing
from utils.utils import get_game, end_game


class Force(commands.Cog):
    def __init__(self, bot):
        self.bot: AmongUs = bot

    @commands.command(name="fmute")
    @commands.has_guild_permissions(mute_members=True)
    @commands.bot_has_guild_permissions(mute_members=True)
    @commands.cooldown(1, 10, BucketType.channel)
    @is_in_voice()
    async def force_mute(self, ctx):
        """Force mute everyone in the voice channel."""

        voice: VoiceState = ctx.author.voice

        for member in voice.channel.members:
            await member.edit(mute=True)

        await ctx.send(f"**{len(voice.channel.members)}** Members in channel **{voice.channel.name}** mute.")

    @commands.command(name="funmute")
    @commands.has_guild_permissions(mute_members=True)
    @commands.bot_has_guild_permissions(mute_members=True)
    @is_in_voice()
    async def force_unmute(self, ctx):
        """Force unmute everyone in the voice channel."""

        voice: VoiceState = ctx.author.voice

        for member in voice.channel.members:
            await member.edit(mute=False)

        await ctx.send(f"**{len(voice.channel.members)}** Members in channel **{voice.channel.name}** unmute.")

    @commands.command(name="fundeafen")
    @commands.has_guild_permissions(deafen_members=True)
    @commands.bot_has_guild_permissions(deafen_members=True)
    @is_in_voice()
    async def force_undeafen(self, ctx):
        """Force undeafen everyone in the voice channel."""

        voice: VoiceState = ctx.author.voice

        for member in voice.channel.members:
            await member.edit(deafen=False)

        await ctx.send(f"**{len(voice.channel.members)}** Members in channel **{voice.channel.name}** undeafened.")

    @commands.command(name="fendgame")
    @is_playing()
    async def force_end_game(self, ctx):
        game = await get_game(self.bot.games, ctx)
        await end_game(game)
        self.bot.games.remove(game)

        await ctx.send("Game has ended.")

    @force_mute.error
    @force_unmute.error
    @force_undeafen.error
    async def force_error(self, ctx, error):
        if isinstance(error, VoiceNotConnected):
            return await ctx.send(error)

        if isinstance(error, BotMissingPermissions):
            return await ctx.send(error)

        if isinstance(error, MissingPermissions):
            return await ctx.send(error)

        if isinstance(error, CommandInvokeError):
            return await ctx.send(error)

        traceback.print_exc()


def setup(bot):
    bot.add_cog(Force(bot))
