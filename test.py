import json
import importlib

import tweepy

from twitty import *
#importlib.reload(twitty)


bot = TwitterBot('test')

#bot.search_tweets('test', '민팅 klay -nftart -filter:links -filter:replies -filter:retweets')

i = 0

class StreamTwitter(tweepy.Stream):
    def on_data(self, status):
        global i
        i += 1
        print(json.loads(status)['text'])

    def on_exception(self, exception):
        print(exception)

st = StreamTwitter(bot.api_key, bot.api_secret, bot.access_token, bot.access_secret)
#st.filter(track=['민팅 klay -nftart -has:links -is:reply -is:retweet'])
st.filter(follow=[1493097742016839682])
print(i)

class TStreamTwitter(tweepy.StreamingClient):
    def on_data(self, status):
        print(json.loads(status)['data']['text'])


#tsc = TStreamTwitter(bot.bearer_token)
#print(tsc.add_rules(tweepy.StreamRule('(민팅 OR 에어드랍) -nftart -is:reply -is:retweet', tag="test")))
#print(tsc.delete_rules('1498281142113665031'))
#tsc.add_rules(tweepy.StreamRule('민팅'))

