import json
import pickle
import numpy as np
import random
from nltk.tokenize import RegexpTokenizer, word_tokenize, TreebankWordTokenizer
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

def topic_model(texts, n_topic):
	#Build the dictionary given the list of words
	dictionary = corpora.Dictionary(texts)
	
	#Build the coupus given list of words
	corpus = [dictionary.doc2bow(t) for t in texts]

	#Compute the TFIDF
	print "Extracting TFIDF..."
	tfidf = models.TfidfModel(corpus)
	corpus_tfidf = tfidf[corpus]

	#Train LDA model
	print "LDA Training..."
	lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=n_topic)

	n_words = 15

	keyterms = []

	for i in range(0, n_topic):
		temp = lda.show_topic(i, n_words)
		#print "TOPIC %d"%(i),
		keyterms.append([])
		for term in temp:
			keyterms[-1].append( term[1])
		print keyterms[-1]



	#lda.save("LDA.model")

def main():

	dataFile = "dataset2"
	stopwordsFile = "stopwords/english.txt"

	data = read_data(dataFile)
	stopwords = init_stopwords(stopwordsFile)

	texts = clean_texts(data, set(stopwords))

	
	for t in texts:
		for i in t:
			if "facebooktwitterlinkedingoogleemailprint" == i:
				print t

	print texts

	topic_model(texts, 30)


if __name__ == "__main__":
	main()

