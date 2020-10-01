from discord import Embed, Message, Emoji, PartialEmoji, Guild
from discord.ext import commands
from discord.ext.commands import Context

from main import AmongUs


class Dead(commands.Cog):
    def __init__(self, bot):
        self.bot: AmongUs = bot

    @commands.command()
    async def react(self, ctx: Context):
        embed = Embed()

        # Map as Thumbnail

        embed.add_field(name="Game Phase",
                        value="Lobby\n"
                              "Playing\n"
                              "Emergency\n"
                              "Report")

        embed.add_field(name="WARNING",
                        value="You have more than 11 players in the discord voice channel.\n"
                              "This will cause a 3-8 second delay when muting / deafening.",
                        inline=False)

        embed.add_field(name="Player Stats",
                        value="Alive: **{}**\n"
                              "Dead: **{}**\n"
                              "Spectating: **{}**",
                        inline=False)

        embed.add_field(name="Game Status",
                        value="Game Started: **{}**\n"
                              "Emergency: **{}**",
                        inline=False)

        # Strikeout deafened
        embed.add_field(name="Players",
                        value="X: **{}**\n"
                              "XX: **{}**\n"
                              "XXX: **{}**\n"
                              "XXXX: **{}**\n"
                              "XXXXX: **{}**",
                        inline=False)

        # Add reactions
        message: Message = await ctx.send(embed=embed)

        guild: Guild = ctx.guild

        emoji = await guild.fetch_emoji(760412009912467456)
        await message.add_reaction(emoji)

        print(message.reactions)


def setup(bot):
    bot.add_cog(Dead(bot))
