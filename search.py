from twitty import *


bot = TwitterBot('twitty', store_db=True)

#bot.search_tweets('test', '민팅 klay', full=True)
bot.search_tweets('minting', '민팅 klay -nftart -filter:links -filter:replies -filter:retweets')
