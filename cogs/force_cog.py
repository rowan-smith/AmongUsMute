import traceback

from discord import VoiceState
from discord.ext import commands
from discord.ext.commands import BotMissingPermissions, MissingPermissions

from main import AmongUs
from utils import is_in_voice, VoiceNotConnected


class Force(commands.Cog):
    def __init__(self, bot):
        self.bot: AmongUs = bot

    @commands.command(aliases=["forcemute"])
    @commands.has_guild_permissions(mute_members=True)
    @commands.bot_has_guild_permissions(mute_members=True)
    @is_in_voice()
    async def fmute(self, ctx):
        """Force mute everyone in the voice channel."""

        voice: VoiceState = ctx.author.voice

        for member in voice.channel.members:
            await member.edit(mute=True)

        await ctx.send(f"**{len(voice.channel.members)}** Members in channel **{voice.channel.name}** mute.")

    @commands.command(aliases=["forceunmute"])
    @commands.has_guild_permissions(mute_members=True)
    @commands.bot_has_guild_permissions(mute_members=True)
    @is_in_voice()
    async def funmute(self, ctx):
        """Force unmute everyone in the voice channel."""

        voice: VoiceState = ctx.author.voice

        for member in voice.channel.members:
            await member.edit(mute=False)

        await ctx.send(f"**{len(voice.channel.members)}** Members in channel **{voice.channel.name}** unmute.")

    @commands.command(aliases=["forceundeafan"])
    @commands.has_guild_permissions(deafen_members=True)
    @commands.bot_has_guild_permissions(deafen_members=True)
    @is_in_voice()
    async def fundeafen(self, ctx):
        """Force undeafen everyone in the voice channel."""

        voice: VoiceState = ctx.author.voice

        for member in voice.channel.members:
            await member.edit(deafen=False)

        await ctx.send(f"**{len(voice.channel.members)}** Members in channel **{voice.channel.name}** undeafened.")

    @fmute.error
    @funmute.error
    @fundeafen.error
    async def force_error(self, ctx, error):
        if isinstance(error, VoiceNotConnected):
            return await ctx.send(error)

        if isinstance(error, BotMissingPermissions):
            return await ctx.send(error)

        if isinstance(error, MissingPermissions):
            return await ctx.send(error)

        traceback.print_exc()


def setup(bot):
    bot.add_cog(Force(bot))
