from typing import Union, List

from discord import VoiceChannel, Member, TextChannel
from discord.ext.commands import Context

from utils.Game import Game


class GameHandler:
    def __init__(self):
        self._games: List[Game] = []

    def create_game(self, ctx: Context) -> Game:
        """Create and add Game to handler

        :param ctx: the Context which has passed
        :return: new Game that was created
        """
        game = Game(ctx.author.voice, ctx.channel, ctx.author)
        self._games.append(game)
        return game

    def get_game(self, identifier: Union[VoiceChannel, TextChannel, Member]) -> Game:
        """Returns the Game the identifier is apart of

        :param identifier: the Game identifying argument
        :return: Game
        """
        if isinstance(identifier, TextChannel):
            for game in self._games:
                if game.is_text_channel(identifier):
                    return game
        if isinstance(identifier, VoiceChannel):
            for game in self._games:
                if game.is_voice_channel(identifier):
                    return game
        if isinstance(identifier, Member):
            for game in self._games:
                if game.is_playing(identifier):
                    return game

    def end_game(self, ctx: Context) -> bool:  ...

    def reset_game(self, ctx: Context) -> bool: ...

    def pause_game(self, ctx: Context) -> bool: ...

    def resume_game(self, ctx: Context) -> bool: ...