import importlib

from twitty import *
#importlib.reload(twitty)


bot = TwitterBot('test')

bot.search_tweets('test', '민팅 klay -nftart -filter:links -filter:replies -filter:retweets')
