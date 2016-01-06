#!/usr/bin/env python
# encoding: utf-8

import csv
import allTweetRetriever
import allAttributes
import appendToCsv
import tweetParser
import reply
import os.path

if __name__ == '__main__':

	fo = open("../twitterpagename.txt", "r+")
	screen_name = fo.read()
	fo.close()

	# Retrieve all the tweets for twitter page name mentioned in twitterpagename.txt file
	tweets = allTweetRetriever.get_all_tweets(screen_name)
	# Listing all the attributes present in tweet statues returned by twitter api
	listOfAttributes = allAttributes.listOfAllAttributes(tweets)

	# Creating file if not present to dump all the data given by twitter
	filename = '../Data/%s_all_tweets_data.csv' % screen_name
	if not os.path.exists(filename):
		with open(filename, 'wb') as f:
			writer = csv.writer(f)
			writer.writerow(listOfAttributes)

	# store the twitter data into outtweets list
	outtweets = []
	for tweet in tweets:
		line = []
		for c in listOfAttributes:
			element = getattr(tweet, c, "")
			try:
				element = element.encode('utf8', 'ignore')
			except:
				pass
			line.append(element)
		outtweets.append(line)
	appendToCsv.appendToCsvFile(filename,outtweets[::-1])

	# Specifying the list of attributes to be extracted
	attributes = ["id","in_reply_to_status_id","retweeted","created_at","text","favorite_count","retweet_count","geo","usermentions","hashtags","current_author","original_authour"] #,"retweeters"]

	# creating file if not present to store extracted data
	filename = '../Data/%s_extracted_tweets_data.csv' % screen_name
	if not os.path.exists(filename):
		with open(filename, 'wb') as f:
			writer = csv.writer(f)
			writer.writerow(attributes)

	# Parsing the twitter data
	parsedData = tweetParser.parsetweet(tweets,attributes)
	# Storing the twitter data
	appendToCsv.appendToCsvFile(filename,parsedData[::-1])

	# Retrieving the replies
	reply.getAllReplies(tweets,attributes,screen_name)
