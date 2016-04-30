from sklearn import svm # no idea why but if sklearn is imported sklearn.svm doesn't work
import numpy as np
from collections import defaultdict

SAMPLE_NAME = 'sample5 Attributes and Time Discrepencies t-0mins'

with open(SAMPLE_NAME+'.csv', 'r') as src:
    # columns we want to load from the csv
    colstouse = [5, 7, 10, 14]
    # numpy txt loading command, note parameters to handle headers and missing values
    data = np.genfromtxt(fname=src, names=True, delimiter=',', missing_values=['-100', '-50', ''],
                         filling_values=None, usecols=colstouse, skip_header=0, dtype=int)
    X = [data['PollTimeWeekday'], data['PollTimeHour'], data['TimeToNext']]
colnames = data.dtype.names
print colnames
print X

'''
Quite a lot of transformations had to be made to bludgeon the data into working
1. we take the 3 input columns lists and put them in a list (X)
2. this list is turned into a matrix (Xm)
3. this matrix is turned back into an ndarray, then reshaped to be the same dimensions as y
'''
Xm = np.matrix(X)
#XmA =  Xm.A.reshape(1101,3) # below command should do this but without needing to be adjusted
XmA =  Xm.A.reshape(len(data['Discrepancy']), len(colnames)-1)
print XmA


#X = np.array(data['TimeToNext'])






classifier = svm.SVC(gamma=0.001, C=100.)  # create an 'estimator instance'
classifier.fit(X=XmA, y=data['Discrepancy'])
print classifier
print classifier.predict(XmA)


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