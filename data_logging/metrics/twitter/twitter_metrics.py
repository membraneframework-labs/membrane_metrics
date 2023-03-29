from data_logging.metrics.metrics import Metrics
from data_logging.time_series import TimeSeries, TimeSeriesEntry
from config.app_config import AppConfig
from data_logging.metrics.twitter.api_facade.twitter_api import TwitterAPI
from datetime import datetime, date, timedelta
from data_logging.mongodb.collection import MongoCollection
from typing import TypeVar

T = TypeVar("T")


class TwitterMetrics(Metrics):
    username: str = "ElixirMembrane"
    how_many_tweets_to_consider: int = 1000

    def __init__(self, app_config: AppConfig):
        self.bearer_token = app_config.twitter_config.bearer_token
        self.start_datetime = app_config.start_date
        self.end_datetime = app_config.end_date
        self.user_id = TwitterAPI.get_user_id(
            self.bearer_token, TwitterMetrics.username
        )
        
    def get_metric_series(self) -> list[TimeSeries]:
        return [
            self.__get_cumulative_engagements_number_per_day(),
            self.__get_current_followers_number(),
        ]

    def __get_cumulative_engagements_number_per_day(self) -> TimeSeries:
        tweet_ids = TwitterAPI.get_user_tweet_ids(
            self.user_id, self.bearer_token, TwitterMetrics.how_many_tweets_to_consider
        )
        chunked_tweet_ids = _chunk_list(tweet_ids, 250)
        results = {}
        for tweet_ids_chunk in chunked_tweet_ids:
            cumulative_reactions_number = TwitterAPI.get_engagements_per_day(
                tweet_ids_chunk, self.bearer_token, self.start_datetime, self.end_datetime
            )
            for day in cumulative_reactions_number.keys():
                for hour in cumulative_reactions_number[day].keys():
                    timestamp = datetime.strptime(f"{day}:{hour}", "%y-%m-%d:%H")
                    if timestamp not in results:
                        results[timestamp] = 0
                    results[timestamp] += int(cumulative_reactions_number[day][hour])

        entries = [
            TimeSeriesEntry(timestamp, results[timestamp])
            for timestamp in results.keys()
        ]
        series = TimeSeries(
            MongoCollection.TwitterCumulativeReactionsToRecentTweetsPerDay, entries
        )
        return series

    def __get_current_followers_number(self) -> TimeSeries:
        followers_number = TwitterAPI.get_current_number_of_followers(
            self.user_id, self.bearer_token
        )
        meassurement_date = datetime.now()
        entry = TimeSeriesEntry(meassurement_date, followers_number)
        series = TimeSeries(MongoCollection.TwitterNumberOfFollowers, [entry])
        return series


def _chunk_list(list: list[T], chunk_size: int) -> list[list[T]]:
    return [list[i : i + chunk_size] for i in range(0, len(list), chunk_size)]
