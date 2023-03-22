import requests
from context.twitter_context import TwitterBearerToken
from typing import NewType
from datetime import date

UserId = NewType("user id", str)
Username = NewType("username", str)
TweetId = NewType("tweet id", str)


class TwitterAPI:
    twitter_v2_api_base_url: str = "https://api.twitter.com/2/"
    twitter_engagement_api_base_url: str = (
        "https://data-api.twitter.com/insights/engagement/"
    )

    @staticmethod
    def get_user_id(username: Username, bearer_token: TwitterBearerToken) -> UserId:
        endpoint = TwitterAPI.twitter_v2_api_base_url + f"users/by/username/{username}"
        response = TwitterAPI.__send_get_request(bearer_token, endpoint)
        return response["data"]["id"]

    @staticmethod
    def get_current_number_of_followers(
        user_id: UserId, bearer_token: TwitterBearerToken
    ) -> int:
        params = {"user.fields": "public_metrics"}
        endpoint = TwitterAPI.twitter_v2_api_base_url + f"users/{user_id}"
        response = TwitterAPI.__send_get_request(bearer_token, endpoint, params)
        return int(response["data.public_metrics"]["followers_count"])

    @staticmethod
    def get_engagements_per_day(
        tweet_ids: list[TweetId],
        bearer_token: TwitterBearerToken,
        start_datetime: date,
        end_datetime: date,
    ) -> dict:
        if len(tweet_ids) > 250:
            raise Exception("Cannot send a request for more than 250 tweet IDs")
        endpoint = TwitterAPI.twitter_engagement_api_base_url + "/totals"
        body = {
            "start": start_datetime.strftime("%Y-%m-%d"),
            "end": end_datetime.strftime("%Y-%m-%d"),
            "tweet_ids": tweet_ids,
            "engagement_types": [
                "impressions",
                "engagements",
                "favorites",
                "quote_tweets",
            ],
            "groupings": {
                "timeline_grouping": {"group_by": ["engagement.day", "engagement.hour"]}
            },
        }
        response = TwitterAPI.__send_post_request(bearer_token, endpoint, data=body)
        return response["timeline_grouping"]

    @staticmethod
    def get_user_tweet_ids(
        user_id: UserId, bearer_token: TwitterBearerToken, how_many_results: int = 100
    ) -> list[TweetId]:
        return TwitterAPI.__get_user_tweet_ids(user_id, bearer_token, how_many_results)

    @staticmethod
    def __get_user_tweet_ids(
        user_id: UserId,
        bearer_token: TwitterBearerToken,
        how_many_results: int,
        pagination_token: str = None,
    ) -> list[TweetId]:
        max_results = min(how_many_results, 100)
        params = {"max_results": max_results}
        if pagination_token:
            params["pagination_token"] = pagination_token
        endpoint = TwitterAPI.twitter_v2_api_base_url + f"users/{user_id}/tweets"
        response = TwitterAPI.__send_get_request(bearer_token, endpoint, params)

        if len(response["data"]) > how_many_results:
            tweets = response["data"][:how_many_results]
        else:
            tweets = response["data"]

        this_response_tweet_ids = []
        for tweet in tweets:
            this_response_tweet_ids.append(tweet["id"])

        if len(response["data"]) < max_results:
            return this_response_tweet_ids
        else:
            next_pagination_token = response["meta"]["next_token"]
            return this_response_tweet_ids + TwitterAPI.__get_number_of_reactions(
                user_id,
                bearer_token,
                how_many_results - len(tweets),
                next_pagination_token,
            )

    @staticmethod
    def __send_get_request(
        bearer_token: TwitterBearerToken, endpoint: str, params: dict = {}
    ) -> dict:
        header = {"Authorization": f"Bearer {bearer_token}"}
        response = requests.get(endpoint, headers=header, params=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def __send_post_request(
        bearer_token: TwitterBearerToken, endpoint: str, params: dict = {}
    ) -> dict:
        header = {"Authorization": f"Bearer {bearer_token}"}
        response = requests.post(endpoint, headers=header, params=params)
        response.raise_for_status()
        return response.json()
