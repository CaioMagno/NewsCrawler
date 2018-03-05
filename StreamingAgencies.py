from Twitterbot_files.NewswireIds import *
from Twitterbot_files.credentials import *
from Twitterbot_files.Twitterbot import *
from Twitterbot_files.DatabaseUtils import *
import tweepy

def storePastTweets(agency, numTweets):
    db_connection = DatabaseConnector("localhost", "root", "12345", "twitter_database")
    stored_tweet_ids = db_connection.getUniqueNewswireTweetIdsForAnAgency(agency.name)
    new_tweets_counter = 0
    for status in tweepy.Cursor(api.user_timeline, id=agency.id).items(numTweets):
        tweet = NewswireTweet(status)
        if tweet.tweetId not in stored_tweet_ids:
            new_tweets_counter += 1
            rows = db_connection.insertNewswireTweet(tweet)
            if rows > 0:
                print("Novo tweet armazenado: ")
                print(tweet.newsAgency, "(", tweet.date, "): ", tweet.content)
    print("\n\nTotal de tweets armazenados: ", new_tweets_counter)


print("Robo para pegar os tweets antigos na timeline das agências")
print("Autenticação da API do Twitter")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

for agency in newswire_list:
    storePastTweets(agency, 500)
