import json

import twitter
from env.keys_and_tokens import *


twitter_api = twitter.Api(consumer_key=api_key, consumer_secret=api_secret, access_token_key=access_token, access_token_secret=access_secret)


'''
account = '@meta_kongz'
print(twitter_api.GetUserTimeline(screen_name=account, count=100, include_rts=False, exclude_replies=False))
'''

query = '민팅 klay -nftart -filter:links -filter:replies -filter:retweets'
#keyword_necesary = ['민팅']
tweets = twitter_api.GetSearch(term=query, count=10000)
#[print(tweets[i].text+'\n'+'-'*60) for i in range(len(tweets))]
for tweet in tweets:
    print(f'id: {tweet.id}')
    print(f'Project: {tweet.user.name}')
    print(f'Agenda: {tweet.text}')
    print('-'*40)


'''
query = ['nft', 'minting']

stream = twitter_api.GetStreamFilter(track=query)
while True:
    for tweets in stream:
        try:
            print(tweets['text'])
            print('-------------------------------------')

        except Exception as e:
            print(e)
            break
'''
