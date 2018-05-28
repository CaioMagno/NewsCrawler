from Twitterbot_files import credentials
import tweepy


def twitter_connect():
    auth = tweepy.OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
    auth.set_access_token(credentials.access_token, credentials.access_token_secret)

    api = tweepy.API(auth)
    
    return auth, api