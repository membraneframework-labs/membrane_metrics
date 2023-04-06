from enum import Enum
from typing import Optional


class MongoCollection(Enum):
    DiscordMembersAtDay = "DiscordMembersAtDay"
    DiscordMessagesPerDayPerChannel = "DiscordMessagesPerDayPerChannel"
    HexCumulativePackagesDownloads = "HexCumulativePackagesDownloads"

    def get_value_field_name(self) -> str:
        match self:
            case MongoCollection.DiscordMembersAtDay:
                return "members_at_day"
            case MongoCollection.DiscordMessagesPerDayPerChannel:
                return "messages_per_day"
            case MongoCollection.HexCumulativePackagesDownloads:
                return "cumulative_hex_packages_downloads"
            case default:
                raise NotImplementedError(
                    f'get_value_field_name is not implemented for {self} collection')

    def get_meta_field_name(self) -> Optional[str]:
        match self:
            case MongoCollection.DiscordMembersAtDay:
                return None
            case MongoCollection.DiscordMessagesPerDayPerChannel:
                return "channel"
            case default:
                return None

    @staticmethod
    def get_default_value() -> float:
        return 0
