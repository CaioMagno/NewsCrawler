from Twitterbot_files.NewswireIds import *
from Twitterbot_files.credentials import *
from Twitterbot_files.Twitterbot import *
from Twitterbot_files.DatabaseUtils import *
import tweepy
import sys, time

def checkTweetDate(tweet_date, reference_date):
    if tweet_date >= reference_date:
        return True
    else:
        return False

def getTweetDate(tweet):
    return tweet.created_at.strftime("%d/%m/%Y")

def storePastTweets(agency, num_pages, reference_date):
    db_connection = DatabaseConnector("localhost", "root", "12345", "twitter_database")
    stored_tweet_ids = db_connection.getUniqueNewswireTweetIdsForAnAgency(agency.name)
    new_tweets_counter = 0
    for page in tweepy.Cursor(api.user_timeline, id=agency.id).pages(num_pages):
        for status in page:
            tweet = NewswireTweet(status)
            tweet_date = getTweetDate(status)
            if (tweet.tweetId not in stored_tweet_ids) and (checkTweetDate(getTweetDate(status), reference_date)):
                new_tweets_counter += 1
                rows = db_connection.insertNewswireTweet(tweet)
                if rows > 0:
                    print("Novo tweet armazenado: ")
                    print(tweet.newsAgency, "(", tweet.date, "): ", tweet.content)
    print("\n\nTotal de tweets armazenados: ", new_tweets_counter)

def getTweetsByDate(agency, reference_date):
    db_connection = DatabaseConnector("localhost", "root", "12345", "twitter_database")
    stored_tweet_ids = db_connection.getUniqueNewswireTweetIdsForAnAgency(agency.name)
    new_tweets_counter = 0

    num_page = 1
    deadend = False
    while True:
        page = api.user_timeline(id=agency.id, page = num_page)
        print("\nPAGINA ",num_page, "-------------------------------------")
        for status in page:
            tweet = NewswireTweet(status)
            tweet_date = getTweetDate(status)

            if tweet_date < reference_date:
                deadend = True
                break

            if (tweet.tweetId not in stored_tweet_ids):
                new_tweets_counter += 1
                rows = db_connection.insertNewswireTweet(tweet)
                if rows > 0:
                    print("Novo tweet armazenado: ")
                    print(tweet.newsAgency, "(", tweet.date, "): ", tweet.content)

        if num_page%4 == 0:
            print("\n INTERVALO DE REQUISIÇÃO\n\n")
            time.sleep(20)		

        if deadend:
            break
        else:
            num_page += 1

    print("\n\nTotal de tweets armazenados: ", new_tweets_counter)


if len(sys.argv) == 2:
    # num_pages = int(sys.argv[1])
    reference_date = sys.argv[1]

    print("Robo para pegar os tweets antigos na timeline das agências")
    print("Autenticação da API do Twitter")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    for agency in newswire_list:
        # storePastTweets(agency, num_pages, reference_date)
        getTweetsByDate(agency, reference_date)
