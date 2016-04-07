import pandas as pd
import numpy as np
import datetime
import matplotlib.pylab as plt


# Test ability of pandas to parse time series data
def pdt1(csvSource):
    csvFileName = csvSource + '.csv'
    dataFile = pd.read_csv(csvFileName)
    print dataFile

    '''
    print dataFile.names
    for row in dataFile:
        print row[0]
    '''

pdt1("sample2.dbCSV")