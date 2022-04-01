from twitty import *


bot = TwitterBot('twitty', store_db=True)


#bot.add_rules('민팅 klay -nftart -is:reply -is:retweet', "minting_tweets")
#bot.add_rules('에어드랍 (WL OR  퍼블릭 OR KLAY OR 이벤트 OR NFT) -nftart -is:reply -is:retweet ', "airdrop_tweets")
bot.stream_filter()
