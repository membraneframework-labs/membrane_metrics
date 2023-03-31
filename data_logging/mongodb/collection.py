from enum import Enum
from typing import Optional


class MongoCollection(Enum):
    DiscordMembersAtDay = "DiscordMembersAtDay"
    DiscordMessagesPerDayPerChannel = "DiscordMessagesPerDayPerChannel"
    TwitterCumulativeReactionsToRecentTweetsPerDay = (
        "TwitterCumulativeReactionsToRecentTweetsPerDay"
    )
    TwitterNumberOfFollowers = "TwitterNumberOfFollowers"
    HexCumulativePackagesDownloads = "HexCumulativePackagesDownloads"
    GoogleTimeSpentPerDay = "GoogleTimeSpentPerDay"
    GoogleUniqueUsersInTutorialPerDay = "GoogleUniqueUsersInTutorialPerDay"
    GoogleUsersFromTrafficSourcePerDay = "GoogleUsersFromTrafficSourcePerDay"
    GoogleBounceRatePerDay = "GoogleBounceRatePerDay"
    

    def get_value_field_name(self) -> str:
        match self:
            case MongoCollection.DiscordMembersAtDay:
                return "members_at_day"
            case MongoCollection.DiscordMessagesPerDayPerChannel:
                return "messages_per_day"
            case MongoCollection.TwitterCumulativeReactionsToRecentTweetsPerDay:
                return "cumulative_reactions_to_recent_tweets_per_day"
            case MongoCollection.TwitterNumberOfFollowers:
                return "number_of_twitter_followers"
            case MongoCollection.HexCumulativePackagesDownloads:
                return "cumulative_hex_packages_downloads"
            case MongoCollection.GoogleTimeSpentPerDay:
                return "google_time_spent_per_day"
            case MongoCollection.GoogleUniqueUsersInTutorialPerDay:
                return "google_unique_users_in_tutorial_per_day"
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
            case MongoCollection.DiscordMembersAtDay:
                return "channel"
            case MongoCollection.DiscordMessagesPerDayPerChannel:
                return "channel"
            case MongoCollection.GoogleUniqueUsersInTutorialPerDay:
                return "tutorial_name"
            case MongoCollection.GoogleUsersFromTrafficSourcePerDay:
                return "traffic_source"
            case default:
                raise NotImplementedError(
                    f"get_meta_field_name is not implemented for {self} collection"
                )
