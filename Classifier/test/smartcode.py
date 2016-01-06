import numpy,re,random
import math
import itertools
import operator


class smartsolver:

	def __init__(self):
		self.word_dict = {}
		self.word_dict_reverse = {}
		self.pos_dict = {}
		self.pos_dict_reverse = {}
		self.word_count = 0
		self.pos_count = 0
		self.ProbTables = {}
		self.defaultWordProbability = 0.00
		self.cache = {}

	def getFromDict(self,dataDict, mapList):
		try:
			value = reduce(lambda d, k: d[k], mapList, dataDict)
			return value
		except:
			return None

	def most_common(self,L):
		d = {}
		for i in L:
			if i not in d:
				d[i] = 0
			else:
				d[i] += 1
		max = "1"
		maxc = 0
		for i in d:
			if maxc < d[i]:
				max = i
				maxc = d[i]
		return max

	def setInDict(self,given_dataDict, given_maplist, value):
		if len(given_maplist) == 1:
			given_dataDict[given_maplist[0]] = value
		else:
			if given_maplist[0] in given_dataDict:
				newmaplist = given_maplist[1:][:]
				self.setInDict(given_dataDict[given_maplist[0]], newmaplist,value)
			else:
				i=len(given_maplist)-1
				while i > 0:
					new_dict = {given_maplist[i]:value}
					value = new_dict
					i -= 1
				given_dataDict[given_maplist[0]]=value

	def is_number(self,s):
		try:
			float(s)
			return True
		except ValueError:
			return False

	def smarttrain(self,data):

		for (s, gt) in data:
			for word in s:
				if word not in self.word_dict:
					if self.is_number(word):
						self.word_dict["1"] = self.word_count
						self.word_dict_reverse[self.word_count] = "1"
					else:
						self.word_dict[word] = self.word_count
						self.word_dict_reverse[self.word_count] = word
					self.word_count += 1
			for tag in gt:
				if tag not in self.pos_dict:
					self.pos_dict[tag] = self.pos_count
					self.pos_dict_reverse[self.pos_count] = tag
					self.pos_count += 1

		table1 = numpy.zeros(shape=(self.word_count, self.pos_count)).astype(int)

		for (s ,gt) in data:
			for i in range(0, len(s)):
				table1[self.word_dict[s[i]]][self.pos_dict[gt[i]]] += 1
		table8 = table1.sum(axis=1)
		table9 = numpy.zeros(shape=self.word_count).astype(float)
		wordcount = table1.sum()
		for i in range(0, self.word_count):
			table9[i] = float(table8[i])/float(wordcount)
		self.defaultWordProbability = table9.min()


		table3 = table1.sum(axis=0)
		total = 0
		for (s, gt) in data:
			total += len(s)
		table2 = numpy.zeros(shape=(1, self.pos_count)).astype(float)
		for i in range(0,self.pos_count):
			table2[0][i] = float(table3[i])/float(total)

		table4 = numpy.zeros(shape=(self.pos_count, self.pos_count)).astype(float)
		for (s, gt) in data:
			for i in range(1, len(gt)):
				table4[self.pos_dict[gt[i-1]]][self.pos_dict[gt[i]]] += 1
		table5 = table4.sum(axis=1)


		for i in range(0, self.pos_count):
			for j in range(0, self.pos_count):
				table4[i][j]=float(table4[i][j])/float(table5[i])
		table6 = numpy.zeros(shape=(self.pos_count, self.pos_count)).astype(float)
		numpy.copyto(table6, table4)
		table7 = table6.sum(axis = 0)
		for i in range(0, self.pos_count):
			for j in range(0, self.pos_count):
				table6[j][i] = float(table6[j][i])/float(table7[i])

		self.ProbTables["CountWordTag"] = table1
		self.ProbTables["ProbTag"] = table2
		self.ProbTables["CountTag"] = table3
		self.ProbTables["ProbTagSet"] = table4
		self.ProbTables["ProbTagSetTranspose"] = table6
		self.ProbTables["PorbWord"] = table9

		return self.ProbTables

	def naiveAlgo(self, sentence):
		naiveTag = []
		wordTag = {}
		result = []
		for i in range(0, len(sentence)):
			probability = -1
			tag = None
			maxTagValue = ""
			if sentence[i] not in self.word_dict:
				proceed = 1
				if(bool(re.search(r'\d', sentence[i]))) == True:
					proceed = 0
					result.append('1')

				if len(result) > 0 and proceed == 1:
					maxTag = 0
					for j in range(0,self.pos_count):
						prevTag = self.ProbTables["ProbTagSet"][self.pos_dict[result[i-1]]][j]
						if prevTag > maxTag:
							maxTag = prevTag
							maxTagValue = self.pos_dict_reverse[j]

					result.append(maxTagValue)
				elif proceed == 1:
					maxProb = self.ProbTables["ProbTag"].argmax()
					maxTag = self.pos_dict_reverse[maxProb]
					result.append(maxTag)

			else:
				for j in range(0,self.pos_count):
					if i==0:
						prob = float(self.ProbTables["CountWordTag"][self.word_dict[sentence[i]]][j])/float(self.ProbTables["CountTag"][j]) * self.wsi(j)
					else:
						prob = float(self.ProbTables["CountWordTag"][self.word_dict[sentence[i]]][j])/float(self.ProbTables["CountTag"][j]) * self.wsi(j)*self.ProbTables["ProbTagSet"][self.pos_dict[result[-1]]][j]
					if prob > probability:
						probability = prob
						tag = self.pos_dict_reverse[j]
				result.append(tag)
				wordTag[sentence[i]] = tag

		return [[[self.most_common(result)]*len(result)],[]]
		#return [[["1"]*len(sentence)],[]]

	def wsi(self, i):
		return self.ProbTables["ProbTag"][0][i]

	def esiwi(self, tag_index, word):
		if word in self.word_dict:
			word_tag_count = self.ProbTables["CountWordTag"][self.word_dict[word]][tag_index]
			tag_count = self.ProbTables["CountTag"][tag_index]
			return float(word_tag_count)/float(tag_count)
		else:
			return 1.0/12.0

	def psiminus1si(self, tag_index1, tag_index2):
		return self.ProbTables["ProbTagSetTranspose"][tag_index1][tag_index2]
	def psiplus1si(self, tag_index1, tag_index2):
		return self.ProbTables["ProbTagSet"][tag_index1][tag_index2]

	def smartviterbi(self,sentence):
		smarttree = numpy.zeros(shape=(self.pos_count,len(sentence),2))

		for i in range(0, self.pos_count):
			smarttree[i][0][1] = -1

		max = 0
		for i in range(0, self.pos_count):
			value = self.wsi(i)*self.esiwi(i,sentence[0])
			if value > max:
				max = value
			smarttree[i][0][0] = value

		for i in range(0, self.pos_count):
			smarttree[i][0][0] = smarttree[i][0][0]/max


		for t in range(1,len(sentence)):
			max_column = 0
			for s in range(0, self.pos_count):
				max_value = 0
				esiwi = self.esiwi(s,sentence[t])
				if esiwi != 0:
					for olds in range(0, self.pos_count):
						val = smarttree[olds][t-1][0]*self.ProbTables["ProbTagSet"][olds][s]
						if val > max_value:
							max_value = val
							smarttree[s][t][0] = val
							smarttree[s][t][1] = olds
				smarttree[s][t][0] *= esiwi
				if smarttree[s][t][0] > max_column:
					max_column = smarttree[s][t][0]
			for s in range(0, self.pos_count):
				smarttree[s][t][0] = smarttree[s][t][0]/max_column

		max_value = 0
		max_index = 0
		for s in range(0, self.pos_count):
			if smarttree[s][len(sentence)-1][0] > max_value:
				max_value = smarttree[s][len(sentence)-1][0]
				max_index = s

		result = ["1"] * len(sentence)
		result[len(sentence)-1] = self.pos_dict_reverse[max_index]

		t = len(sentence)-1
		while t >= 1:
			max_index = smarttree[max_index][t][1]
			result[t-1] = self.pos_dict_reverse[max_index]
			t -= 1
		return [[[self.most_common(result)]*len(result)], []]

	def gettag(self, WordTag):
		for j in range(1, self.pos_count):
				WordTag[j] = WordTag[j-1] + WordTag[j]

		sum = WordTag[-1]
		if sum == 0:
			for j in range(0, self.pos_count):
				WordTag[j] = 1.0/12.0
		else:
			for j in range(0, self.pos_count):
				WordTag[j] = WordTag[j]/sum

		randomIndex = random.random()
		outputIndex = 0
		for k in range(self.pos_count):
			if randomIndex <= WordTag[k]:
				outputIndex = k
				break
		return self.pos_dict_reverse[outputIndex]

	def smartMcmc(self, sentence, count):
		senlen = len(sentence)
		initialSample = []
		for i in range(0, senlen):
			initialSample.append(self.pos_dict_reverse[random.randint(0,11)])
		WordTag = numpy.zeros(shape=self.pos_count).astype(float)

		SampleList = []
		SampleList.append(initialSample)
		for samples in range(1,count):

			presample = SampleList[-1][:]
			SampleList.append(presample)

			for i in range(0,senlen):
				for j in range(self.pos_count):
					p_t = self.pos_dict[SampleList[-1][i-1]] if (i != 0) else self.pos_count
					n_t = self.pos_dict[SampleList[-1][i+1]] if (i != senlen-1) else self.pos_count
					savedwordtag = self.getFromDict(self.cache, [sentence[i],p_t,j,n_t])
					if savedwordtag is not None:
						for g in range(0, self.pos_count):
							WordTag[g]= savedwordtag[g]
					else:
						psi = self.wsi(j)
						pwisi = self.esiwi(j,sentence[i])
						psiminus1si = self.psiminus1si(p_t,j) if (i != 0) else 1
						psiplus1si = self.psiplus1si(j,n_t) if (i != senlen-1) else 1
						WordTag[j] = psi * pwisi * psiminus1si * psiplus1si
						storing = numpy.zeros(shape=self.pos_count).astype(float)
						for g in range(0, self.pos_count):
							storing[g]=WordTag[g]
						self.setInDict(self.cache,[sentence[i],p_t,j,n_t],storing)
				SampleList[samples][i] = self.gettag(WordTag)

		return SampleList



	def smartMcmcold(self, sentence, count):
		count = count + 5
		initialSample = []
		for i in range(0, len(sentence)):
			initialSample.append(self.pos_dict_reverse[random.randint(0,11)])
		WordTag = numpy.zeros(shape=((len(sentence)), self.pos_count)).astype(float)

		SampleList = []
		SampleList.append(initialSample)
		for samples in range(1,count):
			presample = SampleList[-1][:]
			SampleList.append(presample)
			for j in range(self.pos_count):
				WordTag[0][j] = self.esiwi(j,sentence[0])*self.wsi(j)
				if len(sentence) > 1:
					WordTag[0][j] *= float(self.ProbTables["ProbTagSetTranspose"][j][self.pos_dict[SampleList[-1][1]]])

			for j in range(1, self.pos_count):
				WordTag[0][j] = WordTag[0][j-1] + WordTag[0][j]
			for j in range(0, self.pos_count):
				if WordTag.sum() == 0:
					WordTag[0][j] = 1.0/12.0
				else:
					WordTag[0][j] = WordTag[0][j]/WordTag[0][self.pos_count -1]

			randomIndex = random.random()
			outputIndex = 0
			for k in range(self.pos_count):
				if randomIndex <= WordTag[0][k]:
					outputIndex = k
					break
			SampleList[samples][0] = self.pos_dict_reverse[outputIndex]

			a = range(1,len(sentence))
			random.shuffle(a)
			for i in a:
				for j in range(self.pos_count):
					WordTag[i][j] = self.esiwi(j,sentence[i]) * self.esiwi(j,sentence[i]) * self.wsi(j)
					if i != len(sentence)-1:
						WordTag[i][j] *= float(self.ProbTables["ProbTagSetTranspose"][j][self.pos_dict[SampleList[-1][i+1]]])

				for y in range(self.pos_count):
					if WordTag.sum() == 0:
						WordTag[i][y] = 1.0/12.0
					else:
						WordTag[i][y] = float(float(WordTag[i][y]) / float(WordTag.sum()))

				for j in range(1, self.pos_count):
					WordTag[i][j] = WordTag[i][j-1] + WordTag[i][j]

				randomIndex = random.random()

				outputIndex = 0
				for k in range(self.pos_count):
					if randomIndex <= WordTag[i][k]:
						outputIndex = k
						break

				SampleList[samples][i] = self.pos_dict_reverse[outputIndex]

		return SampleList

	def smartmaxmarginal(self, sentence):
		samplecount = 100
		using = 50
		samples = self.smartMcmc(sentence, samplecount)[-using:]
		countmatrix = numpy.zeros(shape=(len(sentence), self.pos_count), dtype = int)
		for i in range(0,using):
			for j in range(0, len(sentence)):
				countmatrix[j][self.pos_dict[samples[i][j]]] += 1
		tagsum = countmatrix.sum(axis=1)
		tagmax = countmatrix.max(axis=1)
		solution = countmatrix.argmax(axis=1)
		values =[]
		solutiontags = []
		for c in range(0, len(sentence)):
			values.append(float(tagmax[c])/float(tagsum[c]))
			solutiontags.append(self.pos_dict_reverse[solution[c]])
		return [ [ solutiontags], [values] ]

	def smartposterior(self, sentence, label):
		result = 0
		for i in range(0, len(sentence)):
			value = self.esiwi(self.pos_dict[label[i]],sentence[i])
			if value != 0:
				result += math.log(value)
		value = self.wsi(self.pos_dict[label[0]])
		if value != 0:
			result += math.log(value)
		for i in range(1, len(sentence)):
			value = self.ProbTables["ProbTagSet"][self.pos_dict[label[i-1]]][self.pos_dict[label[i]]]
			if value != 0:
				result += math.log(value)
		"""
		for i in range(0, len(sentence)):
			if sentence[i] in self.word_dict:
				value = self.ProbTables["PorbWord"][self.word_dict[sentence[i]]]
			else:
				value = self.defaultWordProbability
			if value != 0:
				result -= math.log(value)
		"""
		return result#self.defaultWordProbability