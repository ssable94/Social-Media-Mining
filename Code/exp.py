"""
File used for performing experiments.
File no longer in use
"""

#!/usr/bin/env python
# encoding: utf-8

# reference https://gist.github.com/yanofsky/5436496

import tweepy  # https://github.com/tweepy/tweepy
import csv

# Twitter API credentials



# Twitter only allows access to a users most recent 3240 tweets with this method
def get_all_tweets(screen_name):

	credentials = {}
	fo = open("../credentials.txt", "r+")
	lines = fo.read()
	for line in lines.split("\n"):
		pair = line.split()
		credentials[pair[0]] = pair[1]
	# Close opend file
	fo.close()
	print credentials

	# authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(credentials['consumer_key'], credentials['consumer_secret'])
	auth.set_access_token(credentials['access_key'], credentials['access_secret'])
	api = tweepy.API(auth)

	# initialize a list to hold all the tweepy Tweets
	alltweets = []

	# make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name=screen_name, count=200)
	#print type(new_tweets)

	# save most recent tweets
	alltweets.extend(new_tweets)

	# save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1

	# keep grabbing tweets until there are no tweets left to grab

	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)

		# all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

		# save most recent tweets
		alltweets.extend(new_tweets)

		# update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1

		print "...%s tweets downloaded so far" % (len(alltweets))

	# write the csv
	attributes = set()
	for tweet in alltweets:
		for c in tweet.__dict__.items():
			attributes.add(c[0])
	attributes = list(attributes)
	outtweets = []
	for tweet in alltweets:
		line=[]
		for c in attributes:
			element = getattr(tweet, c, "")
			try:
				element = element.encode('utf8', 'ignore')
			except:
				pass
			line.append(element)
		outtweets.append(line)
	with open('%s_all_tweets_data.csv' % screen_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(attributes)
		writer.writerows(outtweets)


if __name__ == '__main__':
	# pass in the username of the account you want to download
	fo = open("../twitterpagename.txt", "r+")
	name = fo.read()
	# Close opend file
	fo.close()
	get_all_tweets(name)
