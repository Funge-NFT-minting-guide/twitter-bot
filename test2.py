import json
import importlib

import tweepy

from twitty import *
#importlib.reload(twitty)


bot = TwitterBot('test')

bot.search_tweets('test', '민팅 klay -nftart -filter:links -filter:replies -filter:retweets', store_db=True)

'''
i = 0
class StreamTwitter(tweepy.Stream):
    def on_data(self, status):
        global i
        print(json.loads(status)['text'])
        i += 1

    def on_exception(self, exception):
        print(exception)


st = StreamTwitter(bot.api_key, bot.api_secret, bot.access_token, bot.access_secret)
#st.filter(track=['민팅', '에어드랍'])
st.filter(follow=[1495726538066923523], track=['민팅 사이트'])
print(i)


class TStreamClient(tweepy.StreamingClient):
    def on_data(self, status):
        print(json.loads(status)['data']['text'])
'''

'''
tsc = TStreamClient(bot.bearer_token)
#tsc.add_rules(tweepy.StreamRule('(민팅 OR 에어드랍) -nftart -is:replies -is:retweets'))
tsc.add_rules(tweepy.StreamRule('-filter:links'))
tsc.add_rules(tweepy.StreamRule('-filter:replies'))
tsc.add_rules(tweepy.StreamRule('-filter:retweets'))
tsc.filter()
'''
