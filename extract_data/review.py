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

def get_urbancinefile_review(review_url):
    url = review_url
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    review = soup.find_all('font',class_='articleBody')
    review = review[0]
    review = review.get_text()
    review = review.split(":",2)[1]
    return review

def get_sky_review(review_url):
    url = review_url
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    review = soup.find_all('div',class_='review')
    review = review[0]
    review = review.get_text()
    review = review[::-1].split(".",1)[1][::-1]
    return review

def get_vueweekly_review(review_url):
    url = review_url
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    review = soup.find_all('div',class_='entry-content')
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


if __name__ == '__main__':

    movie_dict = MI.getLinkQuote()
    review_quote_list = []
    print "Links generated!"
    k = 1
    for i in range(len(movie_dict)):
        link = movie_dict[i]['link']
        quote = movie_dict[i]['quote']
        k += 1
        print k
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
            
            elif "www.urbancinefile.com.au" in link:
                review = get_urbancinefile_review(link)
                review_quote_list.append({"quote":quote,"review":review})

            elif "http://skymovies.sky.com" in link:
                review = get_sky_review(link)
                review_quote_list.append({"quote":quote,"review":review})

            elif "www.vueweekly.com" in link:
                review = get_vueweekly_review(link)
                review = initial_clean(review, 
                                       delete_first=False,
                                       delete_last=True,
                                       Grade=False)
                
                review_quote_list.append({"quote":quote,"review":review})
            else:
                pass

        except:
            pass

    pickle.dump(review_quote_list, open("review_quotes3","w"))



