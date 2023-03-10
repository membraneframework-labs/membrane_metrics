from typing import NewType

BotToken = NewType('BotToken', str)
GuildID = NewType('GuildID', str)


class DiscordContext:
    bot_token: BotToken
    guild_id: GuildID

    def __init__(self, discord_token: str, discord_guild_id: str) -> None:
        self.bot_token = discord_token
        self.guild_id = discord_guild_id

    def __str__(self) -> str:
        return f'DiscordContext(\'{self.bot_token}\', \'{self.guild_id}\')'
