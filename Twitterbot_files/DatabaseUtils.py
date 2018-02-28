import pymysql
import traceback
from Twitterbot import *

class DatabaseConnector:
    def __init__(self, server_address, username, password, target_database):
        self.server_address = server_address
        self.username = username
        self.password = password
        self.target_database = target_database

    def connect(self):
        db = pymysql.connect(self.server_address, self.username, self.password, self.target_database)
        return db

    def insertSQLCommand(self, sqlStament, tweet):
        db = self.connect()
        row = 0
        try:
            cursor = db.cursor()
            row = cursor.execute(sqlStament, tweet.getSQLParams())
            db.commit()
            db.close()
        except:
            print("EXCEPTION IN: ", sqlStament, "\n")
            print("TWEET ID: ", tweet.tweetId, "\n")
            print(traceback.format_exc())
            db.rollback()
            db.close()
        return row

    def selectSQLCommand(self, sqlStatement):
        db = self.connect()
        cursor = db.cursor()
        cursor.execute(sqlStatement)
        results = cursor.fetchall()
        db.close()
        return results

    def insertNewswireTweet(self, tweet):
        ids = self.getUniqueNewswireTweetIds()
        if tweet.tweetId in ids:
            print("\n Este artigo já consta na base de dados")
            return 0

        sql = "INSERT INTO newswire_tweets (newswire_tweets_id, news_agency, url, date, content, num_retweets, num_favorites, hashtags) \
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        row = self.insertSQLCommand(sql, tweet)
        return row

    def insertReplyTweet(self, tweet):
        sql = "INSERT INTO reply_tweets (tweets_id, date, place, content, original_tweet_id, hashtags) \
                                            VALUES (%s, %s, %s, %s, %s, %s)"
        row = self.insertSQLCommand(sql, tweet)
        return row

    def getUniqueNewswireTweetIds(self):
        sql = "SELECT newswire_tweets_id FROM newswire_tweets"
        #Get a list of tuples
        ids = self.selectSQLCommand(sql)
        #Transforming in a list
        ids = [i[0] for i in ids]
        return ids