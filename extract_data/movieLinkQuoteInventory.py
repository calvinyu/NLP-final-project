import pickle
##############################
#
# This module extract all the movie quotes
# and their original article links from
# rotten tomatos api
#
# Usage:
# getLinkQuote() returns a list of 
# dictionary of key u'link' and u'quote'
#
##############################
datas = pickle.loads(open('Review_dict', 'r').read())
result = []
for data in datas:
  for review in datas[data]['reviews']:
    
    try:
      link = review['links']['review'] 
      if 'http://www.moviechambers.com' in link or \
          'www.macleans.ca' in link or \
          'www.urbancinefile.com.au' in link or \
          'http://skymovies.sky.com' in link or \
          'www.vueweekly.com' in link or \
          'http://www.flicks.co.nz'in link:
          result.append({'link': link, 'quote':review['quote']})
    except:
      pass
def getLinkQuote():
  global result
  return result
