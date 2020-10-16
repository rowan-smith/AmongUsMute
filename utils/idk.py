from discord import Embed

from utils.Game import Game


def gen_embed(game: Game):
    embed = Embed()

    # Map as Thumbnail

    embed.add_field(name="Game Phase",
                    value=game.state.__str__())

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

    return embed
