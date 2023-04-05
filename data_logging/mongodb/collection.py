from enum import Enum
from typing import Optional


class MongoCollection(Enum):
    DiscordMembersAtDay = "DiscordMembersAtDay"
    DiscordMessagesPerDayPerChannel = "DiscordMessagesPerDayPerChannel"

    def get_value_field_name(self) -> str:
        match self:
            case MongoCollection.DiscordMembersAtDay:
                return "members_at_day"
            case MongoCollection.DiscordMessagesPerDayPerChannel:
                return "messages_per_day"
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
                raise NotImplementedError(
                    f'get_meta_field_name is not implemented for {self} collection')

    @staticmethod
    def get_default_value() -> float:
        return 0
