from discord.ext import commands
from discord.ext.commands import Context

from utils.exceptions import NotPlaying, VoiceNotConnected, AlreadyPlaying


def is_playing():
    def predicate(ctx: Context):
        for game in ctx.bot.games:
            if game.is_playing(ctx.author):
                return True
        raise NotPlaying()
    return commands.check(predicate)


def is_in_voice():
    def predicate(ctx: Context):
        if not ctx.author.voice:
            raise VoiceNotConnected()
        return True
    return commands.check(predicate)


def is_not_playing():
    def predicate(ctx: Context):
        for game in ctx.bot.games:
            if game.is_playing(ctx.author):
                raise AlreadyPlaying()
        return True
    return commands.check(predicate)
