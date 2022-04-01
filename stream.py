from twitty import *


bot = TwitterBot('twitty', store_db=True)


#bot.add_rules('민팅 klay -nftart -is:reply -is:retweet', "minting")
#bot.add_rules('에어드랍 -nftart -is:reply -is:retweet', "airdrop")
bot.stream_filter()
