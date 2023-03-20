from data_logging.metrics.metrics import Metrics
from data_logging.mongodb.time_series import MongoTimeSeries, MongoTimeSeriesEntry
from context.context import Context
from data_logging.twitter.api_facade import TwitterAPI
from datetime import datetime
from data_logging.mongodb.collection import MongoCollection

class TwitterMetrics(Metrics):
    username: str = "ElixirMembrane"
    how_many_tweets_to_consider: int = 1000

    def __init__(self, context: Context):
        self.bearer_token = context.twitter_context.bearer_token
        self.user_id = TwitterAPI.get_user_id(self.bearer_token, TwitterMetrics.username)

    def get_metric_series(self) -> list[MongoTimeSeries]:
        return [
            self.__get_cumulative_reactions_number(),
            self.__get_followers_number()
        ]

    def __get_cumulative_reactions_number(self):
        cumulative_reactions_number = TwitterAPI.get_number_of_reactions(self.user_id, self.bearer_token, TwitterMetrics.how_many_tweets_to_consider)
        meassurement_date = datetime.now()
        entry = MongoTimeSeriesEntry(meassurement_date, cumulative_reactions_number)
        series = MongoTimeSeries(MongoCollection.TwitterCumulativeReactionsToRecentTweets, [entry])
        return series

    def __get_followers_number(self):
        followers_number = TwitterAPI.get_number_of_followers(self.user_id, self.bearer_token)
        meassurement_date = datetime.now()
        entry = MongoTimeSeriesEntry(meassurement_date, followers_number)
        series = MongoTimeSeries(MongoCollection.TwitterNumberOfFollowers, [entry])
        return series