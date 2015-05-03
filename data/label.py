import numpy as np
import pandas as pd
import nltk
import pickle

def get_labels(dataset):
    
    labels = []
    
    for review in dataset:
        for i in range(0,len(review)):
            label = review[i][0] #get label
            labels.append(label)

    return labels

if __name__ == "__main__":
    
    labels_generated = False

    try:
        dataset = raw_input('which dataaset? training, testing or validation? ')
        dataset_path = '../data/'+dataset
        data = pickle.loads(open(dataset_path, 'r').read())
        labels_generated = True
    except:
        pass

    if labels_generated:
        print "hello"
        labels = get_labels(data)
        output_path = dataset+'_labels'
        pickle.dump(labels, open(output_path, 'w'))

