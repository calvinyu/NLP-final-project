import json
import pickle
import numpy as np
import random
import nltk
from nltk.util import ngrams
from nltk.tokenize import RegexpTokenizer, word_tokenize, TreebankWordTokenizer
from nltk.tag import pos_tag
from scipy import sparse
from gensim import corpora, models, similarities

"""
Initialize the stopwords list
Input: the stopwords file path
Return: the list of stopwords
"""
def init_stopwords(file_name):

	fp = open(file_name, "r+")
	stoplist = []

	#Read each line in the stopwords file
	while True:
		stop = fp.readline().replace("\n", "")
		if not stop:
			break
		#Append every stopwords into a list
		stoplist.append(stop)

	fp.close()

	return stoplist


def read_data(filename):

	return pickle.load(open(filename, "r"))


def clean_texts(data, stopwords):

	RE = RegexpTokenizer('[^a-z]', gaps=True)

	cleanData = []
	
	for d in data:
		for s in d:
			cleanData.append( list(set(RE.tokenize(s[1].lower())) - stopwords) )

	return cleanData

def parse_tagset():

	tagset = []

	with open("tagset.txt") as data:
		for d in data:
			tagset.append(d.split()[1])

	pickle.dump(tagset, open("POStagset", "w"))

def gen_POSngram_lexicon(tagsetFile):

	tagset = pickle.load(open(tagsetFile, "r"))

	data = [[], [], []]

	#Unigram
	for i in tagset:
		data[0].append(i)


	#Bigram
	for i in tagset:
		for j in tagset:
			data[1].append(i + "_" + j)

	#Trigram
	for i in tagset:
		for j in tagset:
			for k in tagset:
				data[2].append(i + "_" + j + "_" + k)

	dictionary = corpora.Dictionary(data)

	pickle.dump(dictionary, open("pos/pos_trigram.dict", "w"))


def gen_POS_ngram_corpus(posLex, docs):

	posDocs = []
	posNgramDocs = []

	numSamples = len(docs)
	numFeatures = len(posLex)

	matrix = np.zeros((numSamples, numFeatures))

	#Generate POS documents
	for doc in docs:
		posDocs.append([])
		for item in pos_tag(doc):
			posDocs[-1].append(item[1])

	#Generate POS Ngram documents
	for posDoc in posDocs:
		posNgramDocs.append([])

		for n in range(1, 4):
			posNgram = ngrams(posDoc, n)
			
			for item in posNgram:
				posNgramDocs[-1].append( "_".join(item))

	#TFIDF
	corpus = [posLex.doc2bow(p) for p in posNgramDocs]

	tfidf = models.TfidfModel(corpus)

	corpus_tfidf = tfidf[corpus]

	i = 0
	for sample in corpus_tfidf:
		for item in sample:
			matrix[i][item[0]] = item[1]
		i += 1

	print sparse.csr_matrix(matrix)

	return

def main():

	tagsetFile = "pos/POStagset"
	posLexFile = "pos/pos_trigram.dict"
	dataFile = "dataset2"
	stopwordsFile = "stopwords/english.txt"


	data = read_data(dataFile)
	stopwords = init_stopwords(stopwordsFile)

	docs = clean_texts(data, set(stopwords))

	#parse_tagset()
	
	#gen_POSngram_lexicon(tagsetFile)

	posLex = read_data(posLexFile)

	gen_POS_ngram_corpus(posLex, docs)



if __name__ == "__main__":
	main()

