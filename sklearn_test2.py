from sklearn import svm
import numpy as np
import csv

def writeresults(clfname, clf):
    with open(clfname+' for '+SAMPLE_NAME+'.csv', 'wb') as dest:
        destwriter = csv.writer(dest)
        destwriter.writerow(['Weekday', 'Hour', 'Predicted Discrepancy'])
        for weekday in range(1, 7+1):
            for hour in range(6, 23+1):
                destwriter.writerow([weekday, hour, int(clf.predict([weekday, hour])[0])])
            destwriter.writerow(['', '', ''])

SAMPLE_NAME = 'sample5 Attributes and Time Discrepencies t-1mins'
with open(SAMPLE_NAME+'.csv', 'r') as src:
    # columns we want to load from the csv
    colstouse = [5, 7, 14]  # Add 10 if the TimeToNext is needed too
    # numpy txt loading command, note parameters to handle headers and missing values
    data = np.genfromtxt(fname=src, names=True, delimiter=',', missing_values=['-100', '-50', ''],
                         filling_values=None, usecols=colstouse, skip_header=0, dtype=int,
                         unpack=True, usemask=False)
    print data

input = []
output = []
for row in data:
    if row[2] > 0:
        input.append([row[0], row[1]])
        output.append(row[2])

print 'Input len ', len(input)
print 'Output len ', len(output)

# http://scikit-learn.org/stable/modules/svm.html
ninput = np.matrix(input)
#ninput.reshape(1, -1)
noutput = np.array(output)
noutput.reshape(-1, 1)
print ninput.shape
print noutput.shape
clf = svm.SVC()
clf.fit(X=ninput, y=noutput)
print 'Writing SVM results'
writeresults('SVM Predictions', clf)

regclf = svm.SVR()
regclf.fit(X=ninput, y=noutput)
print 'Writing SVR results'
writeresults('SVR Predictions', regclf)


'''
data = np.genfromtxt(fname=src, names=True, delimiter=',', missing_values=['-100', '-50', ''],
                         filling_values=None, usecols=colstouse, skip_header=0, dtype=int,
                         unpack=True, usemask=True)
'''

