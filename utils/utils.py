from utils import Game, NotPlaying, NoGamesExist


async def get_game(games, ctx) -> Game:
    for game in games:
        if game.is_channel(ctx.author.voice.channel.id):
            return game
        raise NotPlaying()
    raise NoGamesExist()
