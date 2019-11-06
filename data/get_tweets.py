#!/usr/bin/env python
# encoding: utf-8

# This code has logic that includes chunking method to accomodate the current Twitter rate-limitting policy. The settings (block size and sleep time) can be adjusted 
# fot this purpose. Please refer to Twitter rate-limitting policy: https://developer.twitter.com/en/docs/basics/rate-limiting
#
# Twitter credentials are necessary to run this code. 
# Please refer to Twitter developer authentication: https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens
#
# Author: Kim Nguyen
# October 2019

import tweepy
import json
import datetime
import time

#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

def auth_setup():
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
    return api

def read_file(file, block_size):
    block = []
    for line in file:
        block.append(line)
        if len(block) == block_size:
            yield block
            block = []
    if block:
        yield block

def get_tweets(user_api, screen_name):
    #initialize a list to hold all the tweepy Tweets
    alltweets = []  
    
    try:
        #make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = user_api.user_timeline(screen_name = screen_name,count=200, include_rts=False, tweet_mode='extended')

        #save most recent tweets
        alltweets.extend(new_tweets)
    
        #save the id of the oldest tweet less one
        try:
            oldest = alltweets[-1].id - 1

            count=1
            # Getting 5 requests for each user's 200 tweets, shooting for 1K tweets per suer
            while count < 5:
                count += 1
                print("getting tweets before {}".format(oldest))
        
                #all subsiquent requests use the max_id param to prevent duplicates
                new_tweets = user_api.user_timeline(screen_name = screen_name,count=200,include_rts=False, tweet_mode='extended', max_id=oldest)
        
                #save most recent tweets
                alltweets.extend(new_tweets)
        
                #update the id of the oldest tweet less one
                oldest = alltweets[-1].id - 1

            print("...{} tweets downloaded so far".format(len(alltweets)))
    
            outtweets = [(tweet.full_text.encode("utf-8").decode("utf-8"), tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')) for tweet in alltweets]
    
            #write the json
            with open('tweets/@{}.json'.format(screen_name), 'w') as f:
                json.dump(outtweets, f)
                print('tweets/@{}.json was successfully created.'.format(screen_name))
            pass

        except IndexError:
            pass

    except tweepy.TweepError as ex:
        if ex.reason == "Not authorized.":
            pass

if __name__ == '__main__':

    api_user = auth_setup()
    block_size = 9
    with open('user_ids.txt', 'r') as text_file:
    # with open('Remain_to_process.txt', 'r') as text_file:    
        for block in read_file(text_file, block_size):
            for line in block:
                get_tweets(api_user, line.rstrip('\n'))
            # time.sleep(1000)   # sleep for > 15 min, rate-limitting issue
       

 