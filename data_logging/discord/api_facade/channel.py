from enum import Enum
from typing import Optional
from data_logging.discord.api_facade.message import DiscordMessage
from data_logging.discord.api_facade.types import DiscordChannelID
from dataclasses import dataclass


class ChannelType(Enum):
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GUILD_DM = 3
    GUILD_CATEGORY = 4
    GUILD_ANNOUNCEMENT = 5
    ANNOUNCEMENT_THREAD = 10
    PUBLIC_THREAD = 11
    PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13
    GUILD_DIRECTORY = 14
    GUILD_FORUM = 15


@dataclass
class DiscordChannel:
    """
    Represents discord channel https://discord.com/developers/docs/resources/channel#channel-object
    """

    id: DiscordChannelID
    name: str
    type: ChannelType
    parent_id: Optional[str]
    messages: list[DiscordMessage]

    def __init__(self, channel_object_response: dict, channel_messages: list[DiscordMessage]) -> None:
        """Creates DiscordGuildMember object from discord guild member object api response.

        Args:
            channel_object_response (dict): https://discord.com/developers/docs/resources/channel#channel-object
            channel_messages (list[DiscordMessage]): all messages send in this channel
        """

        self.id = DiscordChannelID(channel_object_response['id'])
        self.name = channel_object_response['name']
        self.type = ChannelType(channel_object_response['type'])
        self.parent_id = channel_object_response['parent_id']
        self.messages = channel_messages
