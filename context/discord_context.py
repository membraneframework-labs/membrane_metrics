from typing import NewType
from dataclasses import dataclass

BotToken = NewType('BotToken', str)
GuildID = NewType('GuildID', str)


@dataclass
class DiscordContext:
    bot_token: BotToken
    guild_id: GuildID
