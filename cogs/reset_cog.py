from discord import VoiceState
from discord.ext import commands

from main import AmongUs
from utils import is_playing, is_in_voice
from utils.utils import get_game


class ResetGame(commands.Cog):
    def __init__(self, bot):
        self.bot: AmongUs = bot

    @commands.command(name="resetgame")
    @is_playing()
    @is_in_voice()
    async def reset_game(self, ctx):
        game = await get_game(self.bot.games, ctx)

        for player in game.players:
            await player.edit(mute=False, deafen=False)
        for player in game.dead_players:
            await player.edit(mute=False, deafen=False)
        for player in game.spectating_players:
            await player.edit(mute=False, deafen=False)

        game.reset_game()

        voice: VoiceState = ctx.author.voice
        for member in voice.channel.members:
            game.add_player(member)

        await ctx.send("Game reset!")


def setup(bot):
    bot.add_cog(ResetGame(bot))
