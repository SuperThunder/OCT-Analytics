import pandas as pd
import numpy as np
import datetime
import matplotlib.pylab as plt


# Test ability of pandas to parse time series data
def pdt1(csvSource):
    csvFileName = csvSource + '.csv'
    dataFile = pd.read_csv(csvFileName)
    columnNames = list(dataFile.columns.values)
    print columnNames



pdt1("sample2.dbCSV")