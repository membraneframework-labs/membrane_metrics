from enum import Enum
from typing import Optional


class MongoCollection(Enum):
    DiscordMembersAtDay = "DiscordMembersAtDay"
    DiscordMessagesPerDayPerChannel = "DiscordMessagesPerDayPerChannel"
    HexCumulativePackagesDownloads = "HexCumulativePackagesDownloads"
    GoogleTimeSpentPerDay = "GoogleTimeSpentPerDay"
    GoogleUsersInTutorialPerDay = "GoogleUsersInTutorialPerDay"
    GoogleUsersFromTrafficSourcePerDay = "GoogleUsersFromTrafficSourcePerDay"
    GoogleBounceRatePerDay = "GoogleBounceRatePerDay"

    def get_value_field_name(self) -> str:
        match self:
            case MongoCollection.DiscordMembersAtDay:
                return "members_at_day"
            case MongoCollection.DiscordMessagesPerDayPerChannel:
                return "messages_per_day"
            case MongoCollection.HexCumulativePackagesDownloads:
                return "cumulative_hex_packages_downloads"
            case MongoCollection.GoogleTimeSpentPerDay:
                return "google_time_spent_per_day"
            case MongoCollection.GoogleUsersInTutorialPerDay:
                return "google_users_in_tutorial_per_day"
            case MongoCollection.GoogleUsersFromTrafficSourcePerDay:
                return "google_users_from_traffic_source_per_day"
            case MongoCollection.GoogleBounceRatePerDay:
                return "google_bounce_rate_per_day"
            case default:
                raise NotImplementedError(
                    f"get_value_field_name is not implemented for {self} collection"
                )

    def get_meta_field_name(self) -> Optional[str]:
        match self:
            case MongoCollection.DiscordMessagesPerDayPerChannel:
                return "channel"
            case MongoCollection.GoogleUsersInTutorialPerDay:
                return "tutorial_name"
            case MongoCollection.GoogleUsersFromTrafficSourcePerDay:
                return "traffic_source"
            case default:
                return None

    def get_friendly_name(self) -> str:
        match self:
            case MongoCollection.DiscordMembersAtDay:
                return "Number of Discord users in given day"
            case MongoCollection.DiscordMessagesPerDayPerChannel:
                return "Number of messages in given Discord channel in given day"
            case MongoCollection.HexCumulativePackagesDownloads:
                return (
                    "Cumulative number of Membrane packages downloads up to a given day"
                )
            case MongoCollection.GoogleTimeSpentPerDay:
                return "Avarage session duration in given day"
            case MongoCollection.GoogleUsersInTutorialPerDay:
                return "Number of users visiting given tutorial in given day"
            case MongoCollection.GoogleUsersFromTrafficSourcePerDay:
                return "Number of users from different traffic sources in given day"
            case MongoCollection.GoogleBounceRatePerDay:
                return "Moving average of bounce rate for a given day"
            case default:
                return ""

    @staticmethod
    def get_default_value() -> float:
        return 0
