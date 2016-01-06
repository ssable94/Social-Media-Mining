"""
File contains code by prof. David Crandall
"""

import random
import math
from smartcode import smartsolver

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:

	# Calculate the log of the posterior probability of a given sentence
	#  with a given part-of-speech labeling
	def __init__(self):
		self.ss = smartsolver()

	def posterior(self, sentence, label):
		sentence = list(sentence)
		for i in range(0, len(sentence)):
			if self.ss.is_number(sentence[i]):
				sentence[i] = "1"
		for i in range(0, len(sentence)):
			if self.ss.is_number(sentence[i]):
				sentence[i] = "1"
		return self.ss.smartposterior(sentence,label)
		#return 0

	# Do the training!
	#
	def train(self, data):
		newdata = []
		for a in data:
			newdata.append([list(a[0]),list(a[1])])

		for a in newdata:
			for i in range(0, len(a[0])):
				if self.ss.is_number(a[0][i]):
					#print a
					a[0][i] = "1"
			"""
			for word in s:
				if self.ss.is_number(word):
					word = "1"
			"""
		self.ss.smarttrain(newdata)

	# Functions for each algorithm.
	#
	def naive(self, sentence):
		sentence = list(sentence)
		for i in range(0, len(sentence)):
			if self.ss.is_number(sentence[i]):
				sentence[i] = "1"
		return self.ss.naiveAlgo(sentence)

	def mcmc(self, sentence, sample_count):
		return [ [ [ "1" ] * len(sentence) ] * sample_count, [] ]

	def best(self, sentence):
		return [ [ [ "1" ] * len(sentence)], [] ]

	def max_marginal(self, sentence):
		return [ [ [ "1" ] * len(sentence)], [[0] * len(sentence),] ]

	def viterbi(self, sentence):
		sentence = list(sentence)
		for i in range(0, len(sentence)):
			if self.ss.is_number(sentence[i]):
				sentence[i] = "1"
		return self.ss.smartviterbi(sentence)
		#return [ [ [ "1" ] * len(sentence)], [] ]


	def solve(self, algo, sentence):
		if algo == "Naive":
			return self.naive(sentence)
		elif algo == "Sampler":
			return self.mcmc(sentence, 5)
		elif algo == "Max marginal":
			return self.max_marginal(sentence)
		elif algo == "MAP":
			return self.viterbi(sentence)
		elif algo == "Best":
			return self.best(sentence)
		else:
			print "Unknown algo!"


