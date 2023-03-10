from data_logging.discord.api_facade.api_facade import DiscordAPI
from data_logging.discord.api_facade.channel import DiscordChannel
from data_logging.discord.api_facade.guild_member import DiscordGuildMember
from data_logging.discord.api_facade.types import DiscordGuildID
from context.context import Context
from dataclasses import dataclass


@dataclass
class DiscordGuild:
    """
    Represents discord guild https://discord.com/developers/docs/resources/guild#guild-object
    """
    id: DiscordGuildID
    name: str
    members: list[DiscordGuildMember]
    channels: list[DiscordChannel]

    def __init__(self, context: Context) -> None:
        bot_token = context.discord_context.bot_token
        self.id = DiscordGuildID(context.discord_context.guild_id)
        self.name = context.discord_context.guild_id
        self.members = DiscordAPI.get_guild_members(bot_token, self.id)
        self.channels = DiscordAPI.get_guild_channels(bot_token, self.id)
