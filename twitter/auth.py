from os import getenv
import tweepy

bearer_token = getenv("TWITTER_BEARER_TOKEN")
api_key = getenv("TWITTER_API_KEY")
api_secret = getenv("TWITTER_API_KEY_SECRET")
token = getenv("TWITTER_ACCESS_TOKEN")
token_secret = getenv("TWITTER_ACCESS_TOKEN_SECRET")

api = tweepy.Client(bearer_token, api_key, api_secret, token, token_secret)
