from bs4 import BeautifulSoup
import urllib2
import unicodedata
import movieLinkQuoteInventory as MI
import pickle
import nltk

def get_flicks_blog_review(review_url):
    url = review_url
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    review = soup.find_all('div',class_='content blog-post')
    review = review[0]
    review = review.get_text()
    return review

def get_film4_review(review_url):
    url = review_url
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    review = soup.find_all('div',class_='tab-content tab0')
    review = review[0]
    review = review.get_text()
    return review

def get_macleans_review(review_url):
    url = review_url
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    review = soup.find_all('div',class_='text columns no-image twelve wide-ten centered')
    review = review[0]
    review = review.get_text()
    return review

def get_moviechambers_review(review_url):
    #the first sentence from this movie review is to illustrate plot. should be ruled out.
    url = review_url
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    review = soup.find_all('div',class_='entry-content clearfix')
    review = review[0]
    review = review.get_text()
    return review

def initial_clean(review, delete_first=False, delete_last=False, Grade=False):
    if Grade:
        index = review.index('Grade')
        review = review[:index]

    if delete_first or delete_last:

        review = nltk.sent_tokenize(review)
        
        if delete_first:
            review = review[1:]
        if delete_last:
            review = review[:-1]
        
        cleaned = u''
        for c in review:
            cleaned = cleaned + u' ' + c
    
    else:
        cleaned = review

    return cleaned

def to_file(review, filename):

    review = unicodedata.normalize('NFKD',review).encode('ascii','ignore')

    with open(filename, 'w') as out_file:
        out_file.write("%s" % review)

if __name__ == '__main__':

    movie_dict = MI.getLinkQuote()
    review_quote_list = []
    for i in range(len(movie_dict)):
        link = movie_dict[i]['link']
        quote = movie_dict[i]['quote']
        try:
            if "www.macleans.ca" in link:
                review = get_macleans_review(link)
                review = initial_clean(review,
                                       delete_first=True,
                                       delete_last=True,
                                       Grade=False)
                
                review_quote_list.append({"quote":quote,"review":review})
            elif "www.flicks.co.nz" in link:
                review = get_flicks_blog_review(link)
                review = initial_clean(review, 
                                       delete_first=False,
                                       delete_last=True,
                                       Grade=False)
                
                review_quote_list.append({"quote":quote,"review":review})

            elif "www.moviechambers.com" in link:
                review = get_moviechambers_review(link)
                review = initial_clean(review,
                                       delete_first=True,
                                       delete_last=False,
                                       Grade=True)
                
                review_quote_list.append({"quote":quote,"review":review})
            else:
                pass

        except:
            pass

    pickle.dump(review_quote_list, open("review_quotes2","w"))



