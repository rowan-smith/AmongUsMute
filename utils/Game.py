from typing import List

from discord import VoiceChannel, TextChannel, Member, Embed, Message

from main import AmongUs
from utils.enum.GameState import GameState
from utils.Player import Player
from utils.enum.PlayerState import PlayerState


class Game:
    def __init__(self, voice: VoiceChannel, text: TextChannel, leader: Member, message: Message):
        self.voice_channel: VoiceChannel = voice
        self.text_channel: TextChannel = text
        self.leader: Member = leader
        self.message: Message = message

        self.players: List[Player] = []

        self.state: GameState = GameState.LOBBY

    def set_game_state(self, state: GameState) -> None:
        """Sets the current GameState for the Game

        :param state: GameState that the game should be
        :return: None
        """
        self.state = state

    def get_player(self, player: Player) -> Player:
        """Returns player playing the Game

        :param player: The player who you are getting
        :return: Player
        """
        for i in self.players:
            if player.id == i.id:
                return player

    async def is_alive(self, player: Player) -> bool:
        """Returns if a player is alive in game

        :param player: the Member we are checking is alive
        :return: True if player is alive, otherwise False
        """
        for i in self.players:
            if player.id == i.id:
                return player.state == PlayerState.ALIVE
        return False

    async def is_dead(self, player: Player) -> bool:
        """Returns if a player is dead in game

        :param player: the Member we are checking is dead
        :return: True if the player is dead, otherwise False
        """
        for i in self.players:
            if player.id == i.id:
                return player.state == PlayerState.DEAD
        return False

    async def is_spectating(self, player: Player) -> bool:
        """Returns if a player is spectating the game

        :param player: the Member we are checking is spectating
        :return: True if the player is spectating, otherwise False
        """
        for i in self.players:
            if player.id == i.id:
                return player.state == PlayerState.SPECTATING
        return False

    async def is_playing(self, player: Player, include_spectators=True) -> bool:
        """Returns if a member is playing

        :param player: the Member we are checking is playing
        :param include_spectators: should spectators be included?
        :return: True if the player is playing, otherwise False
        """
        if include_spectators:
            return await self.is_alive(player) or await self.is_dead(player) or await self.is_spectating(player)
        else:
            return await self.is_alive(player) or await self.is_dead(player)

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

    async def is_leader(self, player: Player) -> bool:
        """Checks if Member is a leader of the Game

        :param player: Member that is being checked
        :return: True if Member is the leader, otherwise False
        """
        return self.leader.id == player.id

    async def new_player(self, player: Player) -> bool:
        """Adds a player to the game

        :param player: the Member who is being added
        :return: True if the player was added to the Game, otherwise False
        """
        if not await self.is_playing(player):
            self.players.append(player)
            return True
        return False

    async def kill_player(self, player: Player) -> bool:
        """Kills a player moving them from alive to dead

        :param player: the Member who is dead
        :return: True if member is now dead, otherwise False
        """
        if await self.is_alive(player):
            player: Player = self.get_player(player)
            player.state = PlayerState.DEAD
            return True
        return False

    async def revive_player(self, player: Player) -> bool:
        """Revives a player moving them from dead to alive

        :param player: the Member who is being revived
        :return: True if the Member was revived, otherwise False
        """
        if await self.is_dead(player):
            player: Player = self.get_player(player)
            player.state = PlayerState.ALIVE
            return True
        return False

    async def spectate_player(self, player: Player) -> bool:
        """Adds player as spectator

        :param player: the Member who is becoming a spectator
        :return: True if the Member is now spectating, otherwise False
        """
        if await self.is_spectating(player):
            player: Player = self.get_player(player)
            player.state = PlayerState.SPECTATING
            return True
        return False

    async def remove_player(self, player: Player) -> bool:
        """Remove a player from the game completely

        :param player: the Member who should be removed
        :return: True if member was removed, otherwise False
        """
        if await self.is_playing(player):
            player: Player = self.get_player(player)
            self.players.remove(player)
            return True
        return False

    async def reset(self) -> None:
        """Reset the game back to default"""
        self.players = []
        self.state = GameState.LOBBY

    async def get_player_count(self) -> int:
        """Returns the total player count in game

        :return: Number of spectators, dead and alive
        """
        return len(self.players)

    async def get_alive(self) -> List[Player]:
        """Gets all alive players

        :return: Alive players
        """
        return [i for i in self.players if i.state is PlayerState.ALIVE]

    async def get_dead(self) -> List[Player]:
        """Gets all dead players

        :return: Dead players
        """
        return [i for i in self.players if i.state is PlayerState.DEAD]

    async def get_spectating(self) -> List[Player]:
        """Gets all spectating players

        :return: Spectating players
        """
        return [i for i in self.players if i.state is PlayerState.SPECTATING]

    async def update_message(self):
        embed = Embed()

        if await self.get_player_count() > 10:
            embed.add_field(name="WARNING",
                            value="You have more than 11 players in the discord voice channel.\n"
                                  "This will cause a 3-8 second delay when muting / deafening.",
                            inline=False)

        embed.add_field(name="Game Stats",
                        value=f"** **\n"
                              f"**Leader:** {self.leader.mention}\n"
                              f"**Voice Channel:** {self.voice_channel.name}\n"
                              f"\n"
                              f"**Game Phase:** {self.state.__str__()}\n"
                              f"\n"
                              f"**Players Stats:**\n"
                              f"Alive: **{len(await self.get_alive())}**\n"
                              f"Dead: **{len(await self.get_dead())}**\n"
                              f"Spectating: **{len(await self.get_spectating())}**\n",
                        inline=False)

        # Strikeout dead
        embed.add_field(name="Players", value="\n".join(f"{i.display_name}" for i in self.players))
        embed.add_field(name="Player State", value="\n".join(f"{i.state.__str__()}" for i in self.players))

        await self.message.edit(embed=embed)

        # emoji = bot.get_emoji(760412009912467456)
        # await self.message.add_reaction(emoji)
