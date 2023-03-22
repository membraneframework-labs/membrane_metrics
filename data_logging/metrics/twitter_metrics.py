from data_logging.metrics.metrics import Metrics
from data_logging.mongodb.time_series import MongoTimeSeries, MongoTimeSeriesEntry
from context.context import Context
from data_logging.twitter.twitter_api import TwitterAPI
from datetime import datetime, date, timedelta
from data_logging.mongodb.collection import MongoCollection
from typing import TypeVar

T = TypeVar("T")


class TwitterMetrics(Metrics):
    username: str = "ElixirMembrane"
    how_many_tweets_to_consider: int = 1000
    how_many_days_back: int = 10

    def __init__(self, context: Context):
        self.bearer_token = context.twitter_context.bearer_token
        self.user_id = TwitterAPI.get_user_id(
            self.bearer_token, TwitterMetrics.username
        )

    def get_metric_series(self) -> list[MongoTimeSeries]:
        return [
            self.__get_cumulative_engagements_number_per_day(),
            self.__get_current_followers_number(),
        ]

    def __get_cumulative_engagements_number_per_day(self) -> MongoTimeSeries:
        tweet_ids = TwitterAPI.get_user_tweet_ids(
            self.user_id, self.bearer_token, TwitterMetrics.how_many_tweets_to_consider
        )
        chunked_tweet_ids = _chunk_list(tweet_ids, 250)
        start_datetime = date.today()
        end_datetime = date.today() - timedelta(days=TwitterMetrics.how_many_days_back)
        results = {}
        for tweet_ids_chunk in chunked_tweet_ids:
            cumulative_reactions_number = TwitterAPI.get_engagements_per_day(
                tweet_ids_chunk, self.bearer_token, start_datetime, end_datetime
            )
            for day in cumulative_reactions_number.keys():
                for hour in cumulative_reactions_number[day].keys():
                    timestamp = datetime.strptime(f"{day}:{hour}", "%y-%m-%d:%H")
                    if timestamp not in results:
                        results[timestamp] = 0
                    results[timestamp] += int(cumulative_reactions_number[day][hour])

        entries = [
            MongoTimeSeriesEntry(timestamp, results[timestamp])
            for timestamp in results.keys()
        ]
        series = MongoTimeSeries(
            MongoCollection.TwitterCumulativeReactionsToRecentTweetsPerDay, entries
        )
        return series

    def __get_current_followers_number(self) -> MongoTimeSeries:
        followers_number = TwitterAPI.get_current_number_of_followers(
            self.user_id, self.bearer_token
        )
        meassurement_date = datetime.now()
        entry = MongoTimeSeriesEntry(meassurement_date, followers_number)
        series = MongoTimeSeries(MongoCollection.TwitterNumberOfFollowers, [entry])
        return series


def _chunk_list(list: list[T], chunk_size: int) -> list[list[T]]:
    return [list[i : i + chunk_size] for i in range(0, len(list), chunk_size)]
