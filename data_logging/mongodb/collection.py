from enum import Enum
from typing import Optional


class MongoCollection(Enum):
    DiscordMembersAtDay = "DiscordMembersAtDay"
    DiscordMessagesPerDayPerChannel = "DiscordMessagesPerDayPerChannel"
    TwitterCumulativeReactionsToRecentTweets = "TwitterCumulativeReactionsToRecentTweets"
    TwitterNumberOfFollowers = "TwitterNumberOfFollowers"

    def get_value_field_name(self) -> str:
        match self:
            case MongoCollection.DiscordMembersAtDay:
                return "members_at_day"
            case MongoCollection.DiscordMessagesPerDayPerChannel:
                return "messages_per_day"
            case MongoCollection.TwitterCumulativeReactionsToRecentTweets:
                return "cumulative_reactions_to_recent_tweets"
            case MongoCollection.TwitterNumberOfFollowers:
                return "number_of_twitter_followers"
            case default:
                raise NotImplementedError(
                    f'get_value_field_name is not implemented for {self} collection')

    def get_meta_field_name(self) -> Optional[str]:
        match self:
            case MongoCollection.DiscordMembersAtDay:
                return "channel"
            case MongoCollection.DiscordMessagesPerDayPerChannel:
                return "channel"
            case default:
                raise NotImplementedError(
                    f'get_meta_field_name is not implemented for {self} collection')
