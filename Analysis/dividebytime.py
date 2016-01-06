from datetime import datetime
import csv

if __name__=="__main__":
	file = open("../twitterpagename.txt", "r")
	screen_name = file.read()
	file.close()

	print screen_name
	d_f = open("../timeline.txt","r")
	times = d_f.readlines()
	ll = datetime.strptime(times[0].rstrip(),'%b %d %Y')
	es = datetime.strptime(times[1].rstrip(),'%b %d %Y')
	ee = datetime.strptime(times[2].rstrip(),'%b %d %Y')
	ul = datetime.strptime(times[3].rstrip(),'%b %d %Y')
	d_f.close()

	file = open("../Data/%s_extracted_tweets_data.csv" % screen_name, "r")
	fileb = open("../Data/%s_b_ed.csv" % screen_name, "wb")
	filed = open("../Data/%s_d_ed.csv" % screen_name, "wb")
	filea = open("../Data/%s_a_ed.csv" % screen_name, "wb")
	writerb = csv.writer(fileb)
	writerd = csv.writer(filed)
	writera = csv.writer(filea)
	reader = csv.reader(file)
	attributes = next(reader)
	writera.writerow(attributes)
	writerb.writerow(attributes)
	writerd.writerow(attributes)
	for i in range(0,len(attributes)):
		if attributes[i] == "created_at":
			created_at_index = i
	for line in reader:
		t = line[created_at_index].split()[0]
		td = datetime.strptime(t,"%Y-%m-%d")
		if td >= ll:
			if td < es:
				writerb.writerow(line)
			elif td <= ee:
				writerd.writerow(line)
			elif td <= ul:
				writera.writerow(line)
	file.close()
	fileb.close()
	filea.close()
	filed.close()
