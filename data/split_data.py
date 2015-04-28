import numpy as np
import pickle

if __name__ == "__main__":
    reviews = pickle.loads(open('dataset','r').read())
    np.random.shuffle(reviews) #shuffle data
    test = reviews[:70] #pick 70 (30%) samples as test dataset
    validation = reviews[70:120] #pick 50 samples as validation dataset
    train = reviews[120:] #pick 115 as training dataset
    pickle.dump(train, open('training','w'))
    pickle.dump(test, open('testing','w'))
    pickle.dump(validation, open('validation','w'))

