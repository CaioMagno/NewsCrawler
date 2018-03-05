from Twitterbot import *
from tweepy import Stream
from tweepy import OAuthHandler
#from credentials import *
from NewswireIds import *

consumer_key = "a0AYMKXUSn6zZDQJLcD3mXdTV"
consumer_secret = "xdiWlfsFtxAUl70KQR1EK9uBYKfGQb7JPpa7rmcW5Ry7x7KMyC"
access_token = "151542784-CFUZMAKst6jzp6FR8qPkltKhpwePgb9mXVRb1y0N"
access_token_secret = "74v6z0oLRjLbhHGNUHqyps9wpGZ77DvJ5pB5u5XlrmIwF"

g1_politica = "31504246"
politica_estadao = "76369002"
folha_poder = "90963197"
uol_politica = "133435134"
o_globo_politica = "156719729"

print("Autenticação da API do Twitter")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

print("Criando um Robô para vigiar os perfis")
listener = TwitterCrawlerRobot(api)
stream = Stream(auth, listener)
print("Robô trabalhando...\n")
stream.filter(follow=[g1_politica, politica_estadao, folha_poder, uol_politica, o_globo_politica], async=True)
