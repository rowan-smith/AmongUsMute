from discord import VoiceState

from utils import Game, NotPlaying, NoGamesExist


async def get_game(games, ctx) -> Game:
    for game in games:
        if game.is_channel(ctx.author.voice.channel):
            return game
        raise NotPlaying()
    raise NoGamesExist()


async def create_game(games, ctx) -> Game:
    voice: VoiceState = ctx.author.voice
    game = Game(voice.channel)

    # add players in voice chat to game
    for member in voice.channel.members:
        await member.edit(mute=False, deafen=False)
        game.add_player(member)

    games.append(game)
    return game


async def pause_game(game: Game, ctx) -> None:
    try:
        for player in game.players:
            await player.edit(deafen=True)
    except Exception:
        pass

    try:
        for player in game.dead_players:
            await player.edit(mute=False)
    except Exception:
        pass

    try:
        for player in game.spectating_players:
            await player.edit(mute=False)
    except Exception:
        pass

    await ctx.send(f"**{len(game.players)}** Living players have been deafened.\n"
                   f"**{len(game.dead_players) + len(game.spectating_players)}"
                   f"** Dead / Spectating players unmuted.")


async def resume_game(game, ctx) -> None:
    # dead and spectating players are muted
    try:
        for player in game.dead_players:
            await player.edit(mute=True)
    except Exception:
        pass

    try:
        for player in game.spectating_players:
            await player.edit(mute=True)
    except Exception:
        pass

    try:
        for player in game.players:
            await player.edit(deafen=False)
    except Exception:
        pass

    await ctx.send(f"**{len(game.players)}** players have been undeafened.\n"
                   f"**{len(game.dead_players) + len(game.spectating_players)}"
                   f"** Dead / Spectators players muted.")


async def end_game(game) -> None:
    for player in game.players:
        try:
            await player.edit(mute=False, deafen=False)
        except Exception:
            pass
    for player in game.dead_players:
        try:
            await player.edit(mute=False, deafen=False)
        except Exception:
            pass
    for player in game.spectating_players:
        try:
            await player.edit(mute=False, deafen=False)
        except Exception:
            pass
