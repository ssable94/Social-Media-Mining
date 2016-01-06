import retweeters

def gethashtags(tweet):
	hashtags = []
	if "quoted_status" in tweet._json:#[ a for (a,b) in tweet.__dict__.items()]:
		#print "hi"
		for c in tweet._json["quoted_status"]["entities"]["hashtags"]:
			hashtags.append(c["text"])
	if "entities" in tweet._json:#[ a for (a,b) in tweet.__dict__.items()]:
		#print "hi"
		for c in tweet._json["entities"]["hashtags"]:
			hashtags.append(c["text"])
	result = ""
	if hashtags:
		result = hashtags[0]
	for i in range(1, len(hashtags)):
		result += ","+hashtags[i]
	return result


def getusermentions(tweet):
	usermentions = []
	if "quoted_status" in tweet._json:#[ a for (a,b) in tweet.__dict__.items()]:
		#print "hi"
		for c in tweet._json["quoted_status"]["entities"]["user_mentions"]:
			usermentions.append(c["screen_name"])
	if "entities" in tweet._json:#[ a for (a,b) in tweet.__dict__.items()]:
		#print "hi"
		for c in tweet._json["entities"]["user_mentions"]:
			usermentions.append(c["screen_name"])
	result = ""
	if usermentions:
		result = usermentions[0]
	for i in range(1, len(usermentions)):
		result += ","+usermentions[i]
	return result


def parsetweet(alltweets,attributes):
	outtweets = []
	for tweet in alltweets:
		#if tweet.lang == "en":
		line = []
		for c in attributes:
			if c == "usermentions":
				element = getusermentions(tweet).encode('utf8', 'ignore')
			elif c == "retweeters":
				element = retweeters.get_retweeters(tweet.id)
			elif c == "hashtags":
				element = gethashtags(tweet).encode('utf8', 'ignore')
			elif c == "retweeted":
				if "retweeted_status" in tweet.__dict__.keys():
					element = "True"
				else:
					element = "False"
			elif c == "favorite_count":
				if "retweeted_status" in tweet.__dict__.keys():
					element = tweet.retweeted_status.favorite_count
				else:
					element = getattr(tweet, c, 0)
			elif c == "current_author":
				element = tweet._json["user"]["screen_name"]
			elif c == "original_authour":
				if "retweeted_status" in tweet._json:
					element = tweet._json["retweeted_status"]["user"]["screen_name"]
				else:
					element = tweet._json["user"]["screen_name"]
			else:
				element = getattr(tweet, c, "")
				if c == "text":
					if "retweeted_status" in tweet.__dict__.keys():
						iterator = 0
						while element[iterator] != ':':
							iterator += 1
						element = (element[(iterator+2):]).encode('utf8', 'ignore')
					else:
						element = element.encode('utf8', 'ignore')

			line.append(element)
		outtweets.append(line)
	return outtweets