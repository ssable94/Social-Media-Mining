import csv
import os.path

def mapper(filename,outputfilename):
	if not os.path.isfile(filename):
		return None
	file = open(filename, "r")
	reader = csv.reader(file)
	attributes = next(reader)
	for i in range(0,len(attributes)):
		if attributes[i] == "original_authour":
			original_authour_index = i
		elif attributes[i] == "usermentions":
			usermentions_index = i

	entities = set()
	map = {}
	for line in reader:
		entities.add(line[original_authour_index])
		for c in line[usermentions_index].split(","):
			entities.add(c)
		if line[usermentions_index] != '':
			if line[original_authour_index] not in map:
				map[line[original_authour_index]] = line[usermentions_index].split(",")
			else:
				map[line[original_authour_index]] += line[usermentions_index].split(",")[:]
	graph = []
	graphrow = [""]
	entities = list(entities)
	entities.remove("")
	entitymap = {}
	for i in range(0, len(entities)):
		entitymap[entities[i]] = i
	graphrow = graphrow + entities[:]
	graph.append(graphrow[:])
	for i in range(0, len(entities)):
		del graphrow[:]
		graphrow = [entities[i]]+ [0] * len(entities)
		print graphrow
		if entities[i] in map:
			for j in map[entities[i]]:
				graphrow[entitymap[j]+1] += 1
		graph.append(graphrow[:])
	print len(graph)
	with open(outputfilename, 'wb') as f:
		writer = csv.writer(f)
		writer.writerows(graph)

if __name__ == "__main__":
	fo = open("../twitterpagename.txt", "r+")
	screen_name = fo.read()
	# Close opend file
	fo.close()

	filea = "../Data/%s_a_ed.csv" % screen_name
	fileaout = "../Data/%s_ooi_a_ed.csv" % screen_name
	fileb = "../Data/%s_b_ed.csv" % screen_name
	filebout = "../Data/%s_ooi_b_ed.csv" % screen_name
	filed = "../Data/%s_d_ed.csv" % screen_name
	filedout = "../Data/%s_ooi_d_ed.csv" % screen_name
	fileall = "../Data/%s_extracted_tweets_data.csv" % screen_name
	fileoutall = "../Data/%s_ooi_extracted_tweets_data.csv" % screen_name
	mapper(filea,fileaout)
	mapper(fileb,filebout)
	mapper(filed,filedout)
	mapper(fileall, fileoutall)