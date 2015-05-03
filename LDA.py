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


def remove_stopwords(doc, stopwords):
	newDoc = []
	for w in doc:
		if w not in stopwords:
			newDoc.append(w)
	return newDoc

def clean_texts(data, stopwords):

	reTok = RegexpTokenizer('[^a-z]', gaps=True)

	treebanTok = TreebankWordTokenizer()

	cleanData = []
	
	for d in data:
		cleanData.append([])
		for s in d:
			cleanData[-1].append( remove_stopwords(reTok.tokenize(s[1].lower()), stopwords) ) 

	return cleanData

def topic_model(dictionary, texts, n_topic):
	#Build the dictionary given the list of words
	#dictionary = corpora.Dictionary(texts)
	
	#Group all words in the doc
	groupedTexts = []
	for doc in texts:
		groupedTexts.append([])
		for sent in doc:
			groupedTexts[-1] += sent

	
	#Build the coupus given list of words
	corpus = [dictionary.doc2bow(t) for t in groupedTexts]

	#Compute the TFIDF
	print "Extracting TFIDF..."
	tfidf = models.TfidfModel(corpus)
	corpus_tfidf = tfidf[corpus]

	#Train LDA model
	print "LDA Training..."
	lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=n_topic)

	#Compute the topic prob for whole doc and single sent
	matrix = []
	for i in range(len(texts)):
		for j in range(len(texts[i])):
			docTopicProb = [0 for k in range(n_topic)]
			sentTopicProb = [0 for k in range(n_topic)]
	
			#Topic prob for doc	
			for item in lda[corpus[i]]:
				docTopicProb[item[0]] = item[1]
	
			#Topic prob for sent
			for item in lda[dictionary.doc2bow(texts[i][j])]:
				sentTopicProb[item[0]] = item[1]
			
			matrix += [docTopicProb+sentTopicProb]
			
	print sparse.csr_matrix(matrix)

	"""
	n_words = 100

	keyterms = []

	for i in range(0, n_topic):
		temp = lda.show_topic(i, n_words)
		#print "TOPIC %d"%(i),
		keyterms.append([])
		for term in temp:
			keyterms[-1].append( term[1])
	
	return keyterms
	"""
	#lda.save("LDA.model")


def main():

	dataFile = "dataset2"
	stopwordsFile = "stopwords/english.txt"
	lexFile = "lex/toy.lex"

	data = read_data(dataFile)
	lex = read_data(lexFile)
	stopwords = init_stopwords(stopwordsFile)

	"""
	i = 0
	for d in data:
		for sent in d:
			if sent[0] == 1:
				print sent, i
				i += 1
	"""

	texts = clean_texts(data, stopwords)

	"""
	for t in texts:
		for i in t:
			if "facebooktwitterlinkedingoogleemailprint" == i:
				print t
	"""

	keyterms = topic_model(lex, texts, 20)



if __name__ == "__main__":
	main()

