import traceback

from discord import VoiceState
from discord.ext import commands
from discord.ext.commands import Context, BotMissingPermissions

from main import AmongUs
from utils import Game, is_in_voice, is_not_playing, AlreadyPlaying, VoiceNotConnected


class NewGame(commands.Cog):
    def __init__(self, bot):
        self.bot: AmongUs = bot

    @commands.command(name="newgame")
    @commands.bot_has_guild_permissions(mute_members=True, deafen_members=True)
    @is_in_voice()
    @is_not_playing()
    async def new_game(self, ctx: Context):
        """Creates a new game of Among Us."""

        voice: VoiceState = ctx.author.voice

        game = Game(voice.channel)

        for member in voice.channel.members:
            await member.edit(mute=False, deafen=False)
            game.add_player(member)

        self.bot.games.append(game)
        await ctx.send(f"Created game with **{len(voice.channel.members)}** members")

    @new_game.error
    async def new_game_error(self, ctx, error):
        if isinstance(error, AlreadyPlaying):
            return await ctx.send(error)

        if isinstance(error, VoiceNotConnected):
            return await ctx.send(error)

        if isinstance(error, BotMissingPermissions):
            return await ctx.send(error)

        traceback.print_exc()


def setup(bot):
    bot.add_cog(NewGame(bot))
