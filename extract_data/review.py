from bs4 import BeautifulSoup
import urllib2
import unicodedata
import movieLinkQuoteInventory as MI
import pickle

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
            if "www.film4.com" in link:
                review = get_film4_review(link)
            elif "www.flicks.co.nz" in link:
                review = get_flicks_blog_review(link)
            elif "www.moviechambers.com" in link:
                review = get_moviechambers_review(link)
            else:
                review = get_macleans_review(link)
            review_quote_list.append({"quote":quote,"review":review})

        except:
            pass
    pickle.dump(review_quote_list, open("review_quotes","w"))



