from typing import Union, List

from discord import VoiceChannel, Member, TextChannel
from discord.ext.commands import Context

from utils.Game import Game


class GameHandler:
    def __init__(self):
        self._games: List[Game] = []

    async def create_game(self, ctx: Context) -> Game:
        """Create and add Game to handler

        :param ctx: the Context which has passed
        :return: new Game that was created
        """
        game = Game(ctx.author.voice.channel, ctx.channel, ctx.author)
        self._games.append(game)
        return game

    async def get_game(self, identifier: Union[VoiceChannel, TextChannel, Member]) -> Game:
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

    async def end_game(self, ctx: Context) -> bool:
        """Ends the Game for the VoiceChannel

        :param ctx: discord Context
        :return: True if the Game has ended, otherwise False
        """
        game = await self.get_game(ctx.author)
        await self.reset_game(ctx)

        self._games.remove(game)
        return True

    async def reset_game(self, ctx: Context) -> bool:
        """Resets the game to default settings

        :param ctx: discord Context
        :return: True if the Game has been reset successfully, otherwise False
        """
        game = await self.get_game(ctx.author)

        for alive in await game.get_alive():
            await alive.edit(mute=False, deafen=False)

        for dead in await game.get_dead():
            await dead.edit(mute=False, deafen=False)

        for spectator in await game.get_spectating():
            await spectator.edit(mute=False, deafen=False)

        await game.reset()
        return True

    async def pause_game(self, ctx: Context) -> bool:
        """Pauses the game

        :param ctx: discord Context
        :return: True if the Game has been paused successfully, otherwise False
        """
        game = await self.get_game(ctx.author)
        for alive in await game.get_alive():
            await alive.edit(mute=False, deafen=False)

        for dead in await game.get_dead():
            await dead.edit(mute=True, deafen=False)

        for spectator in await game.get_spectating():
            await spectator.edit(mute=True, deafen=False)

        return True

    async def resume_game(self, ctx: Context) -> bool:
        """Resumes the game

        :param ctx: discord Context
        :return: True if the Game has been resumed successfully, otherwise False
        """
        game = await self.get_game(ctx.author)
        for alive in await game.get_alive():
            await alive.edit(mute=False, deafen=True)

        for dead in await game.get_dead():
            await dead.edit(mute=False, deafen=False)

        for spectator in await game.get_spectating():
            await spectator.edit(mute=False, deafen=False)

        return True
