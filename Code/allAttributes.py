#!/usr/bin/env python
# encoding: utf-8

# Returns the list of all attributes in the tweet statues returned by twitter api
def listOfAllAttributes(tweets):
	attributes = set()
	for tweet in tweets:
		for c in tweet.__dict__.items():
			attributes.add(c[0])
	return list(attributes)
