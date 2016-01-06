#!/usr/bin/env python
# encoding: utf-8


import tweepy  # https://github.com/tweepy/tweepy
from time import sleep
import os.path
import json
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


# Only recent 3240 tweets can be retrived using this method
def get_all_tweets(screen_name):

	if not os.path.isfile("tweetData.json"):
		with open("tweetData.json","wb") as f:
			f.write("{}")

	# Loading the data from tweetData.json into dictionary
	udd = json.load(open("tweetData.json"))
	if screen_name in udd:
		minid = udd[screen_name]
	else:
		minid = 1
	proceed = 1

	# Loading credentials from the credentials.txt file
	credentials = {}
	fo = open("../credentials.txt", "r+")
	lines = fo.read()
	for line in lines.split("\n"):
		pair = line.split()
		credentials[pair[0]] = pair[1]
	fo.close()

	# authorize twitter and initialize tweepy
	auth = tweepy.OAuthHandler(credentials['consumer_key'], credentials['consumer_secret'])
	auth.set_access_token(credentials['access_key'], credentials['access_secret'])
	api = tweepy.API(auth)

	# initialize a list to hold all the tweepy Tweets
	alltweets = []
	new_tweets = []

	# make initial request for most recent tweets (200 is the maximum allowed count)
	while proceed == 1:
		proceed = 0
		try:
			if screen_name[0] == "#" or screen_name[0] == "@":
				new_tweets = api.search(q=screen_name, count=200, since_id=minid)
			else:
				new_tweets = api.user_timeline(screen_name=screen_name, count=200, since_id=minid)
		except tweepy.TweepError as e:
			try:
				if str(e.message[0]["message"]) == "Rate limit exceeded":
					proceed = 1
					for i in range(0, 15):
						sleep(10)
						print "waiting", i
				else:
					print "len of result initial error ", len(alltweets), tweepy.TweepError
					return alltweets
			except:
				print "len of result initial error ", len(alltweets), tweepy.TweepError
				return alltweets

	# save most recent tweets
	alltweets.extend(new_tweets)

	# save the id of the oldest tweet less one
	if alltweets:
		oldest = alltweets[-1].id - 1

	# keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:

		# Use max_id and since_id to retrieve the latest not stored data
		try:
			if screen_name[0] == "#" or screen_name[0] == "@":
				new_tweets = api.search(q=screen_name, count=200, max_id=oldest, since_id=minid)
			else:
				new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, since_id=minid)
		except tweepy.TweepError as e:
			try:
				if str(e.message[0]["message"]) == "Rate limit exceeded":
					for i in range(0, 15):
						sleep(10)
						print "waiting", i
				else:
					print "len of result in while error ", len(alltweets), tweepy.TweepError
					return alltweets
			except:
				print "len of result in while error ", len(alltweets), tweepy.TweepError
				return alltweets
		# save most recent tweets
		alltweets.extend(new_tweets)

		# update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1

		print "...%s tweets downloaded so far" % (len(alltweets))

	print "len of result in without error ", len(alltweets)
	maxid = 0
	for tweet in alltweets:
		if tweet.id > maxid:
			maxid = tweet.id
		tweet.id = str(tweet.id)
	if maxid != 0:
		udd[screen_name]=long(maxid)
		json.dump(udd, open("tweetData.json","wb"), indent=4)
	return alltweets
