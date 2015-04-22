import pickle
import nltk

"""
This module segments the data input to the 
following formats:
  1. 
  [
    [ (tag1, sentense1), (tag2, sentense2), ...]
    [ (tag1, sentense1), (tag2, sentense2), ...]
    ...
  ]
  
  2.
  [sentense1, sentense2, sentense3, ...]

  They are stored in file 'dataset' and 'allSent'

  Example:
  >> import pickle
  >> a = pickle.loads(open('dataset', 'r').read())

"""
def read():
  return pickle.loads(open('extract_data/review_quotes', 'r').read())
def segment(raw):
  sents = nltk.sent_tokenize(raw)
  return sents

if __name__ == "__main__":
  allSentence = []
  rqPairs = read()
  documents = []
  for rq in rqPairs:
    r = rq['review']
    q = rq['quote']
    sents = segment(r)
    doc = []
    for sent in sents:
      allSentence.append(sent)
      if q in sent:
        doc.append((1, sent))
      else:
        doc.append((0, sent))
    documents.append(doc)
  pickle.dump(documents, open('dataset', 'w'))
  pickle.dump(allSentence, open('allSent', 'w'))
