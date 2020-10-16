from enum import Enum


class PlayerState(Enum):
    ALIVE = 1
    DEAD = 2
    SPECTATING = 3
    SPECTATING_PERSISTENT = 4

    def __str__(self):
        return f"{self.name.title()}"
