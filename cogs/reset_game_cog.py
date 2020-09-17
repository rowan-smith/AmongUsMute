from discord import VoiceState
from discord.ext import commands

from main import AmongUs
from utils import is_playing
from utils.utils import get_game, end_game


class ResetGame(commands.Cog):
    def __init__(self, bot):
        self.bot: AmongUs = bot

    @commands.command(name="resetgame", aliases=["reset"])
    @is_playing()
    async def reset_game(self, ctx):
        game = await get_game(self.bot.games, ctx)
        await end_game(game)

        game.reset_game()
        game.running = False

        voice: VoiceState = ctx.author.voice
        for member in voice.channel.members:
            game.add_player(member)

        await ctx.send(f"Game reset for channel **{voice.channel.name}**!")


def setup(bot):
    bot.add_cog(ResetGame(bot))
