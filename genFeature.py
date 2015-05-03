import json
import pickle
import numpy as np
import random
import nltk
from sklearn import preprocessing
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
	stoplist = ["$", "\'\'", "``", "(", ")", ",", "--", ".", ":"]

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


def clean_texts(data):

	cleanData = []

	for d in data:
		for item in d:
			sent = item[1].lower()
			cleanData.append( TreebankWordTokenizer().tokenize(sent) )

	#print cleanData


	"""	
	for d in data:
		for s in d:
			cleanData.append( list(set(RE.tokenize(s[1].lower())) - stopwords) )
	"""
	return cleanData

def parse_tagset():

	tagset = ["$", "\'\'", "``", "(", ")", ",", "--", ".", ":"]

	with open("pos/tagset.txt") as data:
		for d in data:
			tagset.append(d.split()[1])

	pickle.dump(tagset, open("pos/POStagset", "w"))


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

		print doc
		print posDocs[-1]
	
	#Generate POS Ngram documents
	for posDoc in posDocs:
		posNgramDocs.append([])

		#Up to trigram
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


def genLexicon(data):

	tok = TreebankWordTokenizer()

	texts = []
	for doc in data:
		for sent in doc:
			texts.append(tok.tokenize( sent[1].lower() ))

	dictionary = corpora.Dictionary(texts)

	pickle.dump(dictionary, open("lex/toy.lex", "w"))

def removeStopwords(doc, stopwords):
	newDoc = []
	for w in doc:
		if w not in stopwords:
			newDoc.append(w)

	return newDoc

def CosSim(sent, doc, lex):

	s = np.zeros(len(lex))
	d = np.zeros(len(lex))

	for item in sent:
		s[item[0]] = item[1]

	for item in doc:
		d[item[0]] = item[1]


	sLength = np.linalg.norm(s)
	dLength = np.linalg.norm(d)

	if sLength == 0 or dLength == 0:
		return 0

	return sum(s*d)/(sLength*dLength)



def genDocumentFeature(data, lex, stopwords):

	tok = TreebankWordTokenizer()

	matrix = []

	bow = []

	for d in data:
		numSent = len(d)
		texts = []
		#Tokenize the sentence
		for i in range(len(d)):
			texts.append( tok.tokenize( d[i][1].lower() ) )

		#Generate top, last and whole documents
		numSentencesUsed = 3
		top = []
		for i in range(min(len(texts), numSentencesUsed)):
			top += texts[i]

		last = []
		for i in range(min(len(texts), numSentencesUsed)):
			last += texts[len(texts)-i-1]
		
		whole = []
		for i in range(len(texts)):
			whole += texts[i]

		numSentencesinDoc = len(texts)
		numWordsinDoc = len(whole)
	
		bowTop = lex.doc2bow(removeStopwords(top, stopwords))
		bowLast = lex.doc2bow(removeStopwords(last, stopwords))
		bowWhole = lex.doc2bow(removeStopwords(whole, stopwords))

		#Generate Similarity features
		for i in range(len(texts)):
			numWordsinSent = len(texts[i])
			sent = removeStopwords(texts[i], stopwords)

			bowSent = lex.doc2bow(sent)
			bow.append(bowSent)

			#Position in doc, # sent in doc, # words in sent, # w in doc, sim to top, sim to last, sim to whole
			matrix.append([float(i+1)/numSentencesinDoc, numSentencesinDoc, numWordsinSent, numWordsinDoc, CosSim(bowSent, bowTop, lex), CosSim(bowSent, bowLast, lex), CosSim(bowSent, bowWhole, lex)])

	#Generate bow features
	bowMatrix = np.zeros((len(bow), len(lex)))

	tfidf = models.TfidfModel(bow)
	bow_tfidf = tfidf[bow]

	i = 0
	for sent in bow_tfidf:
		for item in sent:
			bowMatrix[i][item[0]] = item[1]
		i += 1	
	
	#Merge
	X = np.concatenate((matrix, bowMatrix), axis=1)

	return sparse.csr_matrix(X)


def standardization_and_fit(X):

	scaler = preprocessing.StandardScaler().fit(X)

	normX = scaler.transform(X)

	print normX
	
def main():

	tagsetFile = "pos/POStagset"
	posLexFile = "pos/pos_trigram.dict"
	dataFile = "dataset2"
	stopwordsFile = "stopwords/english.txt"
	lexFile = "lex/toy.lex"

	data = read_data(dataFile)
	lex = read_data(lexFile)
	stopwords = init_stopwords(stopwordsFile)

	#print sorted(lex.token2id.keys())
	#print len(lex)

	#genLexicon(data)
	
	X = genDocumentFeature(data, lex, stopwords)

	print X

	#standardization_and_fit(matrix)




if __name__ == "__main__":
	main()

