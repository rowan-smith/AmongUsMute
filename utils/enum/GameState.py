from enum import Enum


class GameState(Enum):
    LOBBY = 1
    PLAYING = 2
    EMERGENCY = 3
    REPORT = 4
    END = 5

    def __str__(self):
        return f"{self.name.title()}"
