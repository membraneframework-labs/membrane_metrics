from dataclasses import dataclass
from typing import NewType

BotToken = NewType('BotToken', str)
GuildID = NewType('GuildID', str)


@dataclass
class DiscordContext:
    bot_token: BotToken
    guild_id: GuildID
