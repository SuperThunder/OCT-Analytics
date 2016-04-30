import sklearn
import numpy as np
import csv
from collections import defaultdict

SAMPLE_NAME = 'sample5 Attributes and Time Discrepencies t-0mins'

listdict = defaultdict(list)
with open(SAMPLE_NAME+'.csv', 'r') as src:
    next(src)
    data = np.loadtxt(src)
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