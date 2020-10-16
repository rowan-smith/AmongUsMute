from discord import Member

from utils.enum.PlayerState import PlayerState


class Player:

    def __init__(self, member: Member):
        self.__member: Member = member
        self.id = self.__member.id

        self.state: PlayerState = PlayerState.ALIVE

    def set_state(self, state: PlayerState):
        self.state = state

    def __str__(self):
        return self.__member.__str__()

    def __repr__(self):
        return self.__member.__repr__()

    def __eq__(self, other):
        return self.__member.__eq__(other)

    def __ne__(self, other):
        return self.__member.__ne__(other)

    def __hash__(self):
        return self.__member.__hash__()

    @property
    def status(self):
        return self.__member.status()

    @property
    def mobile_status(self):
        return self.__member.mobile_status()

    @property
    def desktop_status(self):
        return self.__member.desktop_status()

    @property
    def web_status(self):
        return self.__member.web_status()

    def is_on_mobile(self):
        return self.__member.is_on_mobile()

    @property
    def colour(self):
        return self.__member.colour()

    @property
    def color(self):
        return self.__member.color()

    @property
    def roles(self):
        return self.__member.roles()

    @property
    def mention(self):
        return self.__member.mention()

    @property
    def display_name(self):
        return self.__member.display_name

    @property
    def activity(self):
        return self.__member.activity()

    def mentioned_in(self, message):
        return self.__member.mentioned_in(message)

    def permissions_in(self, channel):
        return self.__member.permissions_in(channel)

    @property
    def top_role(self):
        return self.__member.top_role()

    @property
    def guild_permissions(self):
        return self.__member.guild_permissions()

    @property
    def voice(self):
        return self.__member.voice()

    async def ban(self, **kwargs):
        return await self.__member.ban(**kwargs)

    async def unban(self, *, reason=None):
        return await self.__member.unban(reason=reason)

    async def kick(self, *, reason=None):
        return await self.__member.kick(reason=reason)

    async def edit(self, *, reason=None, **fields):
        return await self.__member.edit(reason=reason, **fields)

    async def move_to(self, channel, *, reason=None):
        return await self.__member.move_to(channel, reason=reason)

    async def add_roles(self, *roles, reason=None, atomic=True):
        return await self.__member.add_roles(*roles, reason=reason, atomic=atomic)

    async def remove_roles(self, *roles, reason=None, atomic=True):
        return await self.__member.remove_roles(*roles, reason=reason, atomic=atomic)

    async def send(self, content=None, *, tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None,
                   allowed_mentions=None):
        return await self.__member.send(content, tts=tts, embed=embed, file=file, files=files, delete_after=delete_after,
                                        nonce=nonce, allowed_mentions=allowed_mentions)

    async def trigger_typing(self):
        return await self.__member.trigger_typing()

    def typing(self):
        return self.__member.typing()

    async def fetch_message(self, id):
        return await self.__member.fetch_message(id)

    async def pins(self):
        return await self.__member.pins()

    def history(self, *, limit=100, before=None, after=None, around=None, oldest_first=None):
        return self.__member.history(limit=limit, before=before, after=after, around=around, oldest_first=oldest_first)
