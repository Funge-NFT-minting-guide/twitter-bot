import re
import json
import datetime
import requests
from copy import copy
from  pprint import PrettyPrinter

import tweepy
from bs4 import BeautifulSoup
from pymongo import MongoClient

from env.db_config import *
from env.keys_and_tokens import *


class TwitterBot:
    def __init__(self, db_name):
        self.db_host = copy(db_config['host'])
        self.db_port = copy(db_config['port'])
        self.db_username = copy(db_config['username'])
        self.db_password = copy(db_config['password'])
        self.db_name = db_name
        self.api_key = copy(twitter_config['api_key'])
        self.api_secret = copy(twitter_config['api_secret'])
        self.access_token = copy(twitter_config['access_token'])
        self.access_secret = copy(twitter_config['access_secret'])
        self.bearer_token = copy(twitter_config['bearer_token'])
        self.mongo_client = self.get_connect()
        self.twitter_api = self.get_twitter_api()
        self.twitter_client = tweepy.Client(self.bearer_token)
        self.re_tweet_content_url = re.compile(r'(https:\/\/t\.co\/\w{10})$')
        self.pprinter = PrettyPrinter()


    def get_connect(self):
        return MongoClient(host=self.db_host, port=self.db_port, username=self.db_username, password=self.db_password)


    def insert_one(self, collection, document):
        return self.mongo_client[self.db_name][collection].insert_one(document)


    def get_twitter_api(self):
        auth = tweepy.OAuth1UserHandler(self.api_key, self.api_secret, self.access_token, self.access_secret)
        return tweepy.API(auth)


    def get_strem(self, stream_listener):
        return tweepy.Stream(self.api_key, self.api_secret, self.access_token, self.access_secret, stream_listener)


    def is_exists(self, collection, query):
        return self.mongo_client[self.db_name][collection].find_one(query)


    def structure_tweet(self, tweet):
        t_t = dict()
        t_t['id'] = tweet.id
        t_t['user'] = tweet.user.name
        t_t['profile_image_url'] = tweet.user.profile_image_url
        t_t['text'] = tweet.full_text
        t_t['followers'] = tweet.user.followers_count
        return t_t


    def search_tweets(self, collection, query, store_db=False):
        tweets = self.twitter_api.search_tweets(q=query, tweet_mode='extended')
        
        for tweet in tweets:
            t_t = self.structure_tweet(tweet)
            if store_db:
                if self.is_exists(collection, {'id': tweet.id}):
                    continue
                self.insert_one(collection, t_t)
            self.pprinter.pprint(t_t)





'''
account = '@meta_kongz'
print(twitter_api.GetUserTimeline(screen_name=account, count=100, include_rts=False, exclude_replies=False))

def search_minting(query):
    query = '민팅 klay -nftart -filter:links -filter:replies -filter:retweets'
    #keyword_necesary = ['민팅']
    tweets = twitter_api.GetSearch(term=query, count=10000)
    #[print(tweets[i].text+'\n'+'-'*60) for i in range(len(tweets))]
    for tweet in tweets:
        print(f'id: {tweet.id}')
        print(f'Project: {tweet.user.name}')
        print(f'Agenda: {tweet.text}')
        print('-'*40)
    print(tweets[-2])

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
