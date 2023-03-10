import dateutil.parser as parser

from dataclasses import dataclass
from datetime import datetime
from data_logging.discord.api_facade.user import DiscordUserID
from data_logging.discord.api_facade.types import DiscordMessageID


@dataclass
class DiscordMessage:
    """
    Represents discord message https://discord.com/developers/docs/resources/channel#message-object
    """

    id: DiscordMessageID
    content: str
    author_id: DiscordUserID
    timestamp: datetime

    def __init__(self, message_object_response: dict) -> None:
        """Creates DiscordMessage object from discord message object api response.

        Args:
            api_response (dict): https://discord.com/developers/docs/resources/channel#message-object
            guild_members (dict[DiscordGuildMemberID, DiscordGuildMember]): Used to 
        """

        self.id = DiscordMessageID(message_object_response['id'])
        self.content = message_object_response['content']
        self.author_id = DiscordUserID(message_object_response['author']['id'])
        self.timestamp = parser.parse(message_object_response['timestamp'])
