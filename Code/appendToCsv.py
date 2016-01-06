import csv


# Append the given data to given file
def appendToCsvFile(filename,listToBeDumped):
	with open(filename, 'ab') as f:
		writer = csv.writer(f)
		writer.writerows(listToBeDumped)
