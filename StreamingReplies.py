from Twitterbot_files import NewswireIds, TwitterConnection
from Twitterbot_files.Twitterbot import *

import sys

def stream_replies_for_an_agency(api, name, num_pages, db_connection):
    for page in tweepy.Cursor(api.search, q=name, show_user=True, tweet_mode = "extended").pages(num_pages):
        for status in page:
            if status.in_reply_to_status_id != None:
                success = db_connection.insertReplyTweet(ReplyTweet(status))
                if success > 0:
                    print(status.created_at.date(), ":", status.full_text)

def iterate_over_agencies_profiles(api, num_pages):
    db_connection = DatabaseConnector("localhost", "root", "12345", "twitter_database")
    for agency in NewswireIds.newswire_list:
        print("STREAMING DO PERFIL @", agency.name)
        stream_replies_for_an_agency(api, agency.name, num_pages, db_connection)


if len(sys.argv) == 3:
    agency = sys.argv[1]
    num_pages = int(sys.argv[2])
    auth, api = TwitterConnection.twitter_connect()
    # iterate_over_agencies_profiles(api, num_pages)
    db_connection = DatabaseConnector("localhost", "root", "12345", "twitter_database")
    stream_replies_for_an_agency(api, agency, num_pages, db_connection)
else:
    print("FORNEÇA O NÚMERO DE PAGINAS")
