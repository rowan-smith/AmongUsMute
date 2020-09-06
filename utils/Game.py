from typing import List

from discord import VoiceChannel, Member


class Game:
    def __init__(self, channel: VoiceChannel) -> None:
        self.channel = channel
        self.status = False
        self.started = False

        self.players: List[Member] = []
        self.dead_players: List[Member] = []
        self.spectating_players: List[Member] = []

    def add_player(self, member: Member) -> None:
        self.players.append(member)

    def add_dead_player(self, member: Member) -> None:
        self.players.remove(member)
        self.dead_players.append(member)

    def add_spectator(self, member: Member):
        self.spectating_players.append(member)

    def is_playing(self, member: Member) -> bool:
        for player in self.players:
            if player.id == member.id:
                return True
        for player in self.dead_players:
            if player.id == member.id:
                return True
        return False

    def is_alive(self, member: Member) -> bool:
        for player in self.players:
            if player.id == member.id:
                return True

    def is_spectating(self, member: Member):
        for player in self.spectating_players:
            if player.id == member.id:
                return True

    def reset_game(self) -> None:
        self.status = False
        self.started = False

        self.players.clear()
        self.dead_players.clear()
        self.spectating_players.clear()

    def is_channel(self, channel: VoiceChannel):
        return channel.id == self.channel.id
