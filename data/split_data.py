import numpy as np
import pickle

if __name__ == "__main__":
    reviews = pickle.loads(open('dataset','r').read())
    np.random.shuffle(reviews) #shuffle data
    test = reviews[:60] #pick 60 (30%) samples as test dataset
    train = reviews[60:] #pick 142 as training dataset
    pickle.dump(train, open('training','w'))
    pickle.dump(test, open('testing','w'))

