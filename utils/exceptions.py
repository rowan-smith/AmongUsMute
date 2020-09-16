from discord import VoiceChannel
from discord.ext.commands import CommandError


class AlreadyPlaying(CommandError):
    def __init__(self, channel: VoiceChannel = None):
        if channel is None:
            super().__init__("You are already playing a game!")
        else:
            super().__init__(f"You are already playing a game in **{channel.name}**!")


class VoiceNotConnected(CommandError):
    def __init__(self):
        super().__init__("You are not in a voice channel!")


class NotPlaying(CommandError):
    def __init__(self):
        super().__init__("You are currently not playing a game!")


class NoGamesExist(CommandError):
    def __init__(self):
        super().__init__("No games currently exist in this server!")


class AlreadySpectating(CommandError):
    def __init__(self):
        super().__init__("You are already spectating a game~")
