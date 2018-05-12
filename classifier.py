from sklearn.naive_bayes import GaussianNB
import pandas as pd
import numpy as np

def runClassify(sd,mean,avgH,avgS,avgV):
    #Import CSV
    source = '/home/marknolledo/CC/dataset.csv'
    dataset = np.loadtxt(source, dtype=float, delimiter=",", usecols=(0,1,2,3,4))
    category = np.loadtxt(source, dtype=str, delimiter=",", usecols=5)

    #print(dataset[:,0:5])
    #print(category[:])

    #Naive Bayes classification
    x = dataset[:,0:5]
    y = category[:]
    model = GaussianNB()

    model.fit(x,y)

    predicted = model.predict([[sd,mean,avgH,avgS,avgV]])

    print(predicted)
