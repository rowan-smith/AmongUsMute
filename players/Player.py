from discord import Member


class Player:

    def __init__(self, member: Member):
        self.member = member

    def resume(self): ...

    def pause(self): ...
