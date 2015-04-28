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
def match(s, q):
  length = len(q)
  cnt = 0
  for i in range(0, length-7,7):
    if q[i:i+15] in s:
      cnt += 1
  if cnt > 3:
    return True
  return False

if __name__ == "__main__":
  allSentence = []
  rqPairs = read()
  documents = []
  cnt = 0
  i = 0
  for rq in rqPairs:
    r = rq['review']
    r = r.replace(u'\xa0', u' ')
    r = r.replace(u'\u201c', u'"')
    r = r.replace(u'\u201d', u'"')
    q = rq['quote']
    sents = segment(r)
    doc = []
    i += 1
    cc = 0
    for sent in sents:
      allSentence.append(sent)
      if match(sent, q):
        cnt += 1
        doc.append((1, sent))
      else:
        doc.append((0, sent))
    documents.append(doc)
  print cnt, len(rqPairs)
  pickle.dump(documents, open('dataset', 'w'))
  pickle.dump(allSentence, open('allSent', 'w'))
