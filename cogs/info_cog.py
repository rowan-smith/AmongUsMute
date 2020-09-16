import traceback

from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context

from main import AmongUs
from utils import is_in_voice, VoiceNotConnected, NotPlaying, NoGamesExist, is_playing
from utils.utils import get_game


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot: AmongUs = bot

    @commands.command()
    @is_in_voice()
    @is_playing()
    async def info(self, ctx: Context):
        game = await get_game(self.bot.games, ctx)

        embed = Embed()

        embed.add_field(name="Game Stats",
                        value=f"Alive: {len(game.players)},\n"
                              f"Dead: {len(game.dead_players)},\n"
                              f"Spectating: {len(game.spectating_players)},\n"
                              f"Game Started: {game.started},\n"
                              f"Emergency: {game.running}",
                        inline=False)

        players = "".join(f"\n{i.display_name}" for i in game.players)
        dead = "".join(f"\n{i.display_name}" for i in game.dead_players)
        spectator = "".join(f"\n{i.display_name}" for i in game.spectating_players)
        embed.add_field(name="Players",
                        value=f"{players}"
                              f"{dead}"
                              f"{spectator}")

        players = "".join(f"\nAlive" for i in game.players)
        dead = "".join(f"\nDead" for i in game.dead_players)
        spectator = "".join(f"\nSpectating" for i in game.spectating_players)
        embed.add_field(name="Status",
                        value=f"{players}"
                              f"{dead}"
                              f"{spectator}")

        await ctx.send(embed=embed)

    @info.error
    async def info_error(self, ctx, error):
        if isinstance(error, VoiceNotConnected):
            return await ctx.send(error)

        if isinstance(error, (NotPlaying, NoGamesExist)):
            return await ctx.send(error)

        traceback.print_exc()


def setup(bot):
    bot.add_cog(Info(bot))
