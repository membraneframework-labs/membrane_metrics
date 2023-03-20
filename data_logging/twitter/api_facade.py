import requests
from context.twitter_context import TwitterBearerToken
from functools import reduce

class TwitterAPI:
    twitter_api_base_url = "https://api.twitter.com/2/"

    @staticmethod 
    def get_user_id(username: str, bearer_token: TwitterBearerToken):
        endpoint = f"users/by/username/{username}"
        response = TwitterAPI.__send_get_request(bearer_token, endpoint)
        return response["data"]["id"]

    @staticmethod
    def get_number_of_followers(user_id, bearer_token: TwitterBearerToken):
        params = {"user.fields": "public_metrics"}
        endpoint = f"users/{user_id}"
        response = TwitterAPI.__send_get_request(bearer_token, endpoint, params)
        return response['data.public_metrics']['followers_count']

    @staticmethod
    def get_number_of_reactions(user_id: str, bearer_token: TwitterBearerToken, how_many_results: int = 100):
        return TwitterAPI.__get_number_of_reactions(user_id, bearer_token, how_many_results)
        
    @staticmethod 
    def __get_number_of_reactions(user_id: str, bearer_token: TwitterBearerToken, how_many_results: int, pagination_token: str = None):
        max_results = min(how_many_results, 100)
        params = {"tweet.fields": "public_metrics", "max_results": max_results}
        if pagination_token:
            params["pagination_token"]=pagination_token
        endpoint = f"users/{user_id}/tweets"
        response = TwitterAPI.__send_get_request(bearer_token, endpoint, params)
        
        if len(response["data"]) > how_many_results:
            tweets = response["data"][:how_many_results]
        else:
            tweets = response["data"]
        
        this_response_number_of_reactions = 0
        for tweet in tweets:
            public_metrics = tweet["public_metrics"]
            this_response_number_of_reactions+= \
                public_metrics["retweet_count"] + \
                public_metrics["reply_count"] + \
                public_metrics["like_count"] + \
                public_metrics["quote_count"]

        if len(response["data"])<max_results:
            return this_response_number_of_reactions
        else:
            next_pagination_token = response["meta"]["next_token"]
            return this_response_number_of_reactions+TwitterAPI.__get_number_of_reactions(user_id, bearer_token, how_many_results-len(tweets), next_pagination_token)

    @staticmethod
    def __send_get_request(bearer_token: TwitterBearerToken, endpoint: str, params: dict = {}):
        header = {'Authorization': f'Bearer {bearer_token}'}
        response = requests.get(
            TwitterAPI.twitter_api_base_url + endpoint, headers=header, params=params)
        response.raise_for_status()
        return response.json()