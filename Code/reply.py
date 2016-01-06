import tweetParser
import allTweetRetriever
import csv
import appendToCsv
from os import path


def getAllReplies(tweets, attributes, screen_name):

	parsedData = tweetParser.parsetweet(tweets,["id","in_reply_to_status_id","usermentions"])
	idList = map(long, [a for a,b,c in parsedData])
	replyToIdList = [b for a,b,c in parsedData]
	usermentions = list(set([item for sublist in [c for a,b,c in parsedData] for item in sublist.split(",")]))
	if "" in usermentions:
		usermentions.remove("")

	print "making the file"
	# dumping the data
	filename = '../Data/%s_replyTo_extracted_tweets_data.csv' % screen_name
	if not path.isfile(filename):
		with open(filename, 'wb') as f:
			writer = csv.writer(f)
			writer.writerow(attributes)

	retrievedones = []
	for screenNames in usermentions:
		names = screenNames.split(",")
		repliesTo = []
		for c in names:
			print "Doing for ",c
			retrievedTweets = allTweetRetriever.get_all_tweets(c)
			for tweet in retrievedTweets:
				if tweet.in_reply_to_status_id is not None:
					if long(tweet.in_reply_to_status_id) in idList:
						if tweet.id not in retrievedones:
							retrievedones.append(tweet.id)
							repliesTo.append(tweet)
			parsedReplies = tweetParser.parsetweet(repliesTo,attributes)
		appendToCsv.appendToCsvFile(filename,parsedReplies)