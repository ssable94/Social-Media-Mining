'''
1 - Informational: links to stories from newspapers, outside sources (e.g., below tweets contain links to outside sources)
	Fascinating article by WaPo's Sally Jenkins on the current state of women's basketball:
	Great article on Floyd's alleged $5.9M bet http://www.toddstake.com/2013/06/04/the-floyd-fantasy/ …
	SEC to divide $289 Million:  As long as players don't eat a bagel or wash a car, the earth should stay on its axis.

2 - Promotional: links to in-house material, photos, stories on Olympic.org, etc (e.g.,
	below tweets contain links to Olympic.org content, or photos)

	Who will host the 2018 ? Buenos Aires, Glasgow or Medellin? Just one month to go?
	British bobsledder  is sliding to success. Will the  medalist be  with ?
	Youth Olympic Games at the Tower of London ahead of !
	curlers Tom Howell and Korey Dropkin (USA) have tested out the
		venue:

3 - Interactivity: Direct messages to individuals, calls to action (e.g., first two tweets
	below include calls to action, last tweet is a direct message to an individual)
	We have had a makeover! Go check out our awesome new  website at  and let us know what you think!
	Want to try a new sport? How about biathlon? Watch and learn with  graduate :
	Awesome to meet  at FIS World Cup Final, Lenzerheide.

4 - Diversion: Messages not related to YOG (e.g., below tweets contain non-YOG related content)
	Just made a great nacho dip! #YOG
	#awesome we have over 100,000 followers. Thank you for loving #yog
	Did you know that 8 March is International Women’s Day?

5 - no source

6 - twitter photos
'''

import csv
import nltk


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


def preprocess(line):

	file = open("../twitterpagename.txt", "r")
	screen_name = file.read()
	file.close()

	for i in range(0,len(line)):
		if line[i][:7] == "http://" or line[i][:4] == "www." or line[i][:8] == "https://":
			line[i] = "__url__"
		elif line[i][0] == '@':
			line[i] = "__user__" + line[i][1:]
		elif line[i][0] == '#':
			line[i] = "__hashtag__" + line[i][1:]
		elif isfloat(line[i]):
			line[i] = "__num__"
	return line


def to_tag(tag):
	tag.rstrip()
	if tag == "1":
		return 1
	if tag == "2":
		return 2
	if tag == "3":
		return 3
	if tag == "4":
		return 4
	if tag == "5(no source)":
		return 5
	if tag == "5(Twitter Photo)":
		return 6


if __name__=="__main__":

	file = open("train.csv", "r")
	reader = csv.reader(file)
	Data = []
	taglist={1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
	for line in reader:
		pl = preprocess(line[0].rstrip().decode('utf-8', 'ignore').lower().split())
		tag = to_tag(line[1])
		if tag is not None:
			taglist[tag] += 1
		t_l = ""
		for i in range(0, len(pl)):
			t_l = t_l + str(pl[i])+" "+str(tag)+" "
		t_l.rstrip()
		Data.append(t_l)
	f = open("cleaned.txt","wb")
	for d in Data:
		f.write(d+"\n")
	f.close()
	# This will help in calculating base line
	print taglist
'''
{1: 21, 2: 204, 3: 99, 4: 16, 5: 44, 6: 2}
'''

