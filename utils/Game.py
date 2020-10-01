from typing import List

from discord import VoiceChannel, TextChannel, Member

from utils.GameState import GameState


class Game:
    def __init__(self, voice: VoiceChannel, text: TextChannel, leader: Member):
        self.voice_channel: VoiceChannel = voice
        self.text_channel: TextChannel = text
        self.leader: Member = leader

        self._alive: List[Member] = []
        self._dead: List[Member] = []
        self._spectating: List[Member] = []

        self.state: GameState = GameState.LOBBY

    def set_game_state(self, state: GameState) -> None:
        """Sets the current GameState for the Game

        :param state: GameState that the game should be
        :return: None
        """
        self.state = state

    async def is_alive(self, member: Member) -> bool:
        """Returns if a player is alive in game

        :param member: the Member we are checking is alive
        :return: True if player is alive, otherwise False
        """
        return member in self._alive

    async def is_dead(self, member: Member) -> bool:
        """Returns if a player is dead in game

        :param member: the Member we are checking is dead
        :return: True if the player is dead, otherwise False
        """
        return member in self._dead

    async def is_spectating(self, member: Member) -> bool:
        """Returns if a player is spectating the game

        :param member: the Member we are checking is spectating
        :return: True if the player is spectating, otherwise False
        """
        return member in self._spectating

    async def is_playing(self, member: Member, include_spectators=True) -> bool:
        """Returns if a member is playing

        :param member: the Member we are checking is playing
        :param include_spectators: should spectators be included?
        :return: True if the player is playing, otherwise False
        """
        if include_spectators:
            return await self.is_alive(member) or self.is_dead(member) or self.is_spectating(member)
        else:
            return await self.is_alive(member) or self.is_dead(member)

    async def is_voice_channel(self, voice_channel: VoiceChannel) -> bool:
        """Check if a VoiceChannel is the same as the Game

        :param voice_channel: VoiceChannel that is being checked
        :return: True if the VoiceChannel is the same, otherwise False
        """
        return self.voice_channel.id == voice_channel.id

    async def is_text_channel(self, text_channel: TextChannel) -> bool:
        """Check if a TextChannel is the same as the Game

        :param text_channel: TextChannel that is being checked
        :return: True if the TextChannel is the same, otherwise, False
        """
        return self.text_channel.id == text_channel.id

    async def is_leader(self, member: Member) -> bool:
        """Checks if Member is a leader of the Game

        :param member: Member that is being checked
        :return: True if Member is the leader, otherwise False
        """
        return self.leader.id == member.id

    async def new_player(self, member: Member) -> bool:
        """Adds a player to the game

        :param member: the Member who is being added
        :return: True if the player was added to the Game, otherwise False
        """
        if not self._alive:
            self._alive.append(member)
            return True
        return False

    async def kill_player(self, member: Member) -> bool:
        """Kills a player moving them from alive to dead

        :param member: the Member who is dead
        :return: True if member is now dead, otherwise False
        """
        if self.is_alive(member):
            self._alive.remove(member)
            self._dead.append(member)
            return True
        return False

    async def revive_player(self, member: Member) -> bool:
        """Revives a player moving them from dead to alive

        :param member: the Member who is being revived
        :return: True if the Member was revived, otherwise False
        """
        if self.is_dead(member):
            self._dead.remove(member)
            self._alive.append(member)
            return True
        return False

    async def spectate_player(self, member: Member) -> bool:
        """Adds player as spectator

        :param member: the Member who is becoming a spectator
        :return: True if the Member is now spectating, otherwise False
        """
        if self.is_spectating(member):
            return False

        if self.is_alive(member):
            self._alive.remove(member)

        if self.is_dead(member):
            self._dead.remove(member)

        self._spectating.append(member)
        return True

    async def remove_player(self, member: Member) -> bool:
        """Remove a player from the game completely

        :param member: the Member who should be removed
        :return: True if member was removed, otherwise False
        """
        if self.is_alive(member):
            self._alive.remove(member)
            return True
        if self.is_dead(member):
            self._dead.remove(member)
            return True
        if self.is_spectating(member):
            self._spectating.remove(member)
            return True
        return False

    async def reset(self) -> None:
        """Reset the game back to default"""
        self._alive: List[Member] = []
        self._dead: List[Member] = []
        self._spectating: List[Member] = []

        self.state = GameState.LOBBY

    async def get_player_count(self) -> int:
        """Returns the total player count in game

        :return: Number of spectators, dead and alive
        """
        return len(self._alive) + len(self._dead) + len(self._spectating)

    async def get_alive(self) -> List[Member]:
        """Gets all alive players

        :return: Alive players
        """
        return self._alive

    async def get_dead(self) -> List[Member]:
        """Gets all dead players

        :return: Dead players
        """
        return self._dead

    async def get_spectating(self) -> List[Member]:
        """Gets all spectating players

        :return: Spectating players
        """
        return self._spectating
