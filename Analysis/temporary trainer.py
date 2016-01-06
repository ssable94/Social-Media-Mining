import csv
import nltk


def preprocess(line):

	file = open("../twitterpagename.txt", "r")
	screen_name = file.read()
	file.close()

	print "line", line
	for i in range(0,len(line)):
		if line[i][:7] == "http://" or line[i][:4] == "www." or line[i][:8] == "https://":
			line[i] = "__url__"
		elif line[i][0] == '@':
			line[i] = "__user__" + line[i][1:]
		elif line[i][0] == '#':
			line[i] = "__hashtag__" + line[i][1:]
	print "new_line", line
	return line


f = open("train.txt", "w")
file = open("../Data/%s_extracted_tweets_data.csv" % screen_name, "r")
reader = csv.reader(file)
attributes = next(reader)
for i in range(0,len(attributes)):
	if attributes[i] == "id":
		id_index = i
	elif attributes[i] == "text":
		text_index = i
for line in reader:
	pl = preprocess(line[text_index].decode('utf-8', 'ignore').lower().split())
	f.write([item for sublist in [nltk.word_tokenize(i) for i in pl] for item in sublist])
f.close()