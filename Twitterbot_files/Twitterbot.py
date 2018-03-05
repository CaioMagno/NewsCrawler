from tweepy.streaming import StreamListener
import tweepy
from Twitterbot_files.NewswireIds import *
from Twitterbot_files.DatabaseUtils import DatabaseConnector

# g1_politica = 31504246
# politica_estadao = 76369002
# folha_poder = 90963197
# uol_politica = 133435134
# o_globo_politica = 156719729
#
# newswire_ids = [g1_politica, politica_estadao, folha_poder, uol_politica, o_globo_politica]

class TwitterCrawlerRobot(StreamListener):
    ''' Handles data received from the stream. '''
    def __init__(self, api):
        print("\nIniciando o Robo")
        self.dbConnection = DatabaseConnector('localhost', 'root', '12345', 'twitter_database')
        self.api = api
        StreamListener.__init__(self, api=api)


    def on_status(self, status):
        # Prints the text of the tweet
        if status.author.id in newswire_ids:
            tweet = NewswireTweet(status)
            row = self.dbConnection.insertNewswireTweet(tweet)
            print("\nTweet de notícia da agencia ", tweet.newsAgency,": ", tweet.content)
        elif status.in_reply_to_status_id != None:
            tweet = ReplyTweet(status)
            if status.truncated == True:
                status_extended = self.api.get_status(status.id, tweet_mode = "extended")
                tweet.content = status_extended.full_text
            row = self.dbConnection.insertReplyTweet(tweet)
            print("\nTweet de resposta: ", tweet.content)

            if not self.isOriginalTweetStored(tweet.originalTweetId):
                original_tweet = self.getOriginalTweetForAReply(tweet.originalTweetId)
                row = self.dbConnection.insertNewswireTweet(original_tweet)
                print("\nTweet de notícia da agencia ", original_tweet.newsAgency, ": ", original_tweet.content)

        return True

    def isOriginalTweetStored(self, originalTweetId):
        # Return true if the original tweet was already stored
        ids = self.dbConnection.getUniqueNewswireTweetIds()
        if originalTweetId in ids:
            return True
        else:
            return False

    def getOriginalTweetForAReply(self, originalTweetId):
        return NewswireTweet(self.api.get_status(originalTweetId))

    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True  # To continue listening

    def on_timeout(self):
        print('Timeout...')
        return True  # To continue listening


class Tweet:
    def getSQLParams(self):
        pass

class NewswireTweet(Tweet):
    def __init__(self, status):
        self.tweetId = str(status.id)
        self.newsAgency = status.author.screen_name
        if len(status.entities["urls"]) == 0:
            self.url = ""
        else:
                self.url = status.entities["urls"][0]["url"]
        self.date = status.created_at
        self.content = status.text.replace(self.url, "").replace("'", "\'").replace('"', "\"").encode('utf-8')
        self.retweet_count = status.retweet_count
        self.favorite_count = status.favorite_count
        hashtags = [hashtag['text'] for hashtag in status.entities['hashtags']]
        self.hashtags = ' '.join(hashtags)

    def getSQLParams(self):
        return (self.tweetId, self.newsAgency, self.url, self.date.strftime("%d/%m/%Y"), self.content, self.retweet_count, self.favorite_count, self.hashtags)


class ReplyTweet(Tweet):
    def __init__(self, status):
        self.tweetId = str(status.id)
        self.date = status.created_at
        if status.place != None:
            self.place = status.place.name
        else:
            self.place = ""
        self.content = status.text.replace("'", "\'").replace('"', "\"").encode('utf-8')
        self.originalTweetId = status.in_reply_to_status_id
        hashtags = [hashtag['text'] for hashtag in status.entities['hashtags']]
        self.hashtags = ' '.join(hashtags)

    def getSQLParams(self):
        return (self.tweetId, self.date.strftime("%d/%m/%Y"), self.place, self.content, self.originalTweetId, self.hashtags)
