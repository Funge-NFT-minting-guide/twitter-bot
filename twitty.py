import json
import logging
import  pprint
import datetime
import requests
from copy import copy

import pytz
import tweepy
from pymongo import MongoClient
from dateutil import parser as date_parser

from env.db_config import *
from env.keys_and_tokens import *


logging.basicConfig(filename='/var/log/twitty.log', format='[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] - %(message)s', level=logging.DEBUG)


class StreamingTwitter(tweepy.StreamingClient):
    def __init__(self, bearer_token, bot):
        super().__init__(bearer_token)
        self.bot = bot

    
    def structure_tweet(self, data, includes):
        t_t = dict()
        t_t['id'] = data['id']
        t_t['created_at'] = date_parser.parse(data['created_at']).astimezone(pytz.timezone('Asia/Seoul'))
        t_t['text'] = data['text']
        t_t['user'] = includes['users'][0]['name']
        t_t['uid'] = includes['users'][0]['id']
        t_t['profile_image_url'] = includes['users'][0]['profile_image_url']
        t_t['followers'] = includes['users'][0]['public_metrics']['followers_count']
        t_t['url'] = f"https://twitter.com/{includes['users'][0]['username']}/status/{data['id']}"
        return t_t


    def on_data(self, status):
        status = json.loads(status)
        t_t = self.structure_tweet(status['data'], status['includes'])
        pprint.pprint(t_t)
        collection = status['matching_rules'][0]['tag']

        if self.bot.store_db:
            if self.bot.is_exists(collection, {'id': t_t['id']}):
                return
            self.bot.insert_one(collection, t_t)


class TwitterBot:
    def __init__(self, db_name, store_db=False):
        self.db_host = copy(db_config['host'])
        self.db_port = copy(db_config['port'])
        self.db_username = copy(db_config['username'])
        self.db_password = copy(db_config['password'])
        self.db_name = db_name
        self.store_db = store_db
        self.api_key = copy(twitter_config['api_key'])
        self.api_secret = copy(twitter_config['api_secret'])
        self.access_token = copy(twitter_config['access_token'])
        self.access_secret = copy(twitter_config['access_secret'])
        self.bearer_token = copy(twitter_config['bearer_token'])
        self.mongo_client = self.get_connect()
        self.twitter_api = self.get_twitter_api()
        self.twitter_client = tweepy.Client(self.bearer_token)
        self.twitter_stream = StreamingTwitter(self.bearer_token, self)
        #self.re_tweet_content_url = re.compile(r'(https:\/\/t\.co\/\w{10})$')


    def get_connect(self):
        return MongoClient(host=self.db_host, port=self.db_port, username=self.db_username, password=self.db_password, authSource=self.db_name)


    def insert_one(self, collection, document):
        return self.mongo_client[self.db_name][collection].insert_one(document)


    def get_twitter_api(self):
        auth = tweepy.OAuth1UserHandler(self.api_key, self.api_secret, self.access_token, self.access_secret)
        return tweepy.API(auth)


    def get_strem(self, stream_listener):
        return tweepy.Stream(self.api_key, self.api_secret, self.access_token, self.access_secret, stream_listener)


    def add_rules(self, rule, collection):
        return self.twitter_stream.add_rules(tweepy.StreamRule(rule, tag=collection))


    def stream_filter(self):
        return self.twitter_stream.filter(expansions='author_id', tweet_fields=['created_at'], user_fields=['username', 'profile_image_url', 'public_metrics', 'entities'])


    def is_exists(self, collection, query):
        return self.mongo_client[self.db_name][collection].find_one(query)


    def structure_tweet(self, tweet):
        t_t = dict()
        t_t['id'] = tweet.id_str
        t_t['created_at'] = tweet.created_at.astimezone(pytz.timezone('Asia/Seoul'))
        t_t['user'] = tweet.user.name
        t_t['uid'] = tweet.user.id_str
        t_t['profile_image_url'] = tweet.user.profile_image_url
        t_t['text'] = tweet.full_text
        t_t['followers'] = tweet.user.followers_count
        t_t['url'] = f'https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}'
        return t_t


    def search_tweets(self, collection, query, full=False, store_db=False):
        if not full:
            tweets = self.twitter_api.search_tweets(q=query, count=10000, tweet_mode='extended')
        else:
            tweets = self.twitter_api.search_full_archive('full', query)
        
        for tweet in tweets:
            #self.pprint.pprint(tweet)
            t_t = self.structure_tweet(tweet)
            pprint.pprint(t_t)
            if self.store_db:
                if self.is_exists(collection, {'id': tweet.id_str}):
                    continue
                self.insert_one(collection, t_t)
