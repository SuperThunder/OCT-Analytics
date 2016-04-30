from sklearn import svm # no idea why but if sklearn is imported sklearn.svm doesn't work
import numpy as np
import csv
from collections import defaultdict

SAMPLE_NAME = 'sample5 Attributes and Time Discrepencies t-0mins'

listdict = defaultdict(list)
with open(SAMPLE_NAME+'.csv', 'r') as src:
    #next(src)
    # columns we want to load from the csv
    colstouse = [5, 7, 10, 14]
    # numpy txt loading command, note parameters to handle headers and missing values
    data = np.genfromtxt(fname=src, names=True, delimiter=',', missing_values=['-100', '-50', ''],
                         filling_values=None, usecols=colstouse, skip_header=0, dtype=int)

colnames = data.dtype.names

print colnames
print data

classifier = svm.SVC(gamma=0.001, C=100.) # create an 'estimator instance'
#classifier.fit(X=)


'''
    csv = csv.reader(src)
    columnNames = csv.next()
    print columnNames
    for row in csv:
        #print row
        listdict[row[5]].append([row[6], row[7], row[8], row[14]])

valdict = {}
for key in listdict.keys():
    valdict[key] = listdict[key]
print valdict
'''