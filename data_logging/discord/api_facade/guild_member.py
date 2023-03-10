from datetime import date
from typing import NewType
from data_logging.discord.api_facade.user import DiscordUser
from dataclasses import dataclass
from dateutil.parser import parse


@dataclass
class DiscordGuildMember:
    """
    Represents discord guild member https://discord.com/developers/docs/resources/guild#guild-member-object
    """

    user: DiscordUser
    joined_at: date

    def __init__(self, guild_member_object_response: dict) -> None:
        """Creates DiscordGuildMember object from discord guild member object api response.

        Args:
            guild_member_object_response (dict): https://discord.com/developers/docs/resources/guild#guild-member-object
        """

        self.user = DiscordUser(guild_member_object_response['user'])
        self.joined_at = parse(guild_member_object_response['joined_at']).date()
