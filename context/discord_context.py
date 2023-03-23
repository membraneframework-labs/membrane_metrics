from typing import NewType
from dataclasses import dataclass

BotToken = NewType('BotToken', str)
UserToken = NewType('UserToken', str)
GuildID = NewType('GuildID', str)

@dataclass
class DiscordContext:
    bot_token: BotToken
    user_token: UserToken
    guild_id: GuildID

