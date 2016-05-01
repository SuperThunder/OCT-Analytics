from sklearn import svm # no idea why but if sklearn is imported sklearn.svm doesn't work
import numpy as np

SAMPLE_NAME = 'sample5 Attributes and Time Discrepencies t-2mins'

with open(SAMPLE_NAME+'.csv', 'r') as src:
    # columns we want to load from the csv
    colstouse = [5, 7, 14]  # Add 10 if the TimeToNext is needed too
    # numpy txt loading command, note parameters to handle headers and missing values
    data = np.genfromtxt(fname=src, names=True, delimiter=',', missing_values=['-100', '-50', ''],
                         filling_values=None, usecols=colstouse, skip_header=0, dtype=int)
    print data

clf = svm.SVC(gamma=0.001, C=100.)
#clf.fit(X=data['PollTimeWeekday'], y=data['Discrepancy'])


X = [data['PollTimeWeekday'], data['PollTimeHour']]
colnames = data.dtype.names
print colnames
print X


'''
Quite a lot of transformations had to be made to bludgeon the data into working
Something also seems to have gone wrong in preserving attribute togetherness
1. we take the 3 input columns lists and put them in a list (X)
2. this list is turned into a matrix (Xm)
3. this matrix is turned back into an ndarray, then reshaped to be the same dimensions as y
'''

print 'X', X, '\n\n'
Xr = np.array(X)
Xr.reshape(1, -1)
print Xr
Xm = np.matrix(X)
print Xm
#XmA =  Xm.A.reshape(1101,3)
XmA = Xm.A.reshape(len(data['Discrepancy']), 2)
print 'xma', XmA[700]


#X = np.array(data['TimeToNext'])


classifier = svm.SVC(gamma=0.001, C=100., verbose=False)  # create an 'estimator instance'
classifier.fit(X=XmA, y=data['Discrepancy'])
print classifier
print classifier.predict(XmA)
print classifier.predict([3, 10])


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