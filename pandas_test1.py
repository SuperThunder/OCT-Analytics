import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Test ability of pandas to parse time series data
def pdt1(csvSource):
    csvFileName = csvSource + '.csv'
    dataFile = pd.read_csv(csvFileName, index_col=None, parse_dates=True)
    columnNames = list(dataFile.columns.values)  # Get the column names
    print columnNames
    dataframe = pd.DataFrame(data=dataFile)
    #print dataFrame
    #dataSeries = pd.Series(dataFrame)
    #print dataframe.head(), dataframe.columns
    print dataframe.describe() # gives info on count, mean, std dev, min/max, etc of columns
    plt.show(dataframe.plot())

pdt1("sample5 Attributes and Time Discrepencies t-0mins")