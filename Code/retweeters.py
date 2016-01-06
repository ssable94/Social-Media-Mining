#!/usr/bin/env python
# encoding: utf-8

# reference https://gist.github.com/yanofsky/5436496

import tweepy  # https://github.com/tweepy/tweepy
from time import sleep
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

# Twitter only allows access to a users most recent 3240 tweets with this method
def get_retweeters(tweet_id):

	proceed = 1

	credentials = {}
	fo = open("../credentials.txt", "r+")
	lines = fo.read()
	for line in lines.split("\n"):
		pair = line.split()
		credentials[pair[0]] = pair[1]
	# Close opend file
	fo.close()

	# authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(credentials['consumer_key'], credentials['consumer_secret'])
	auth.set_access_token(credentials['access_key'], credentials['access_secret'])
	api = tweepy.API(auth)

	# initialize a list to hold all the tweepy Tweets
	alltweets = []

	# make initial request for most recent tweets (200 is the maximum allowed count)
	while proceed == 1:
		proceed = 0
		try:
			new_tweets = api.retweets(tweet_id)
		except tweepy.TweepError as e:
			try:
				if str(e.message[0]["message"]) == "Rate limit exceeded":
					proceed = 1
					for i in range(0, 15):
						sleep(10)
						print "waiting", i
				else:
					print "len of result initial error ", len(alltweets), tweepy.TweepError
					print str(e.message[0]["message"])
					return ""
			except:
				print "len of result initial error ", len(alltweets), tweepy.TweepError
				return ""
	result =""
	for c in new_tweets:
		result = result +" "+ c._json["user"]["screen_name"]
	return result

if __name__ =="__main__":
	get_retweeters("669911586958626000")