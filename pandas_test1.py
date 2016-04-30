import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Test ability of pandas to parse time series data
def pdt1(csvSource):
    csvFileName = csvSource + '.csv'
    dateindex = pd.date_range(start='6:00:00 04/02/2016', end='23:00:00 04/25/2016', period=1)
    dataFile = pd.read_csv(csvFileName, parse_dates=True)
    columnNames = list(dataFile.columns.values)  # Get the column names

    print columnNames
    dataframe = pd.DataFrame(data=dataFile)
    tsdf = pd.DataFrame(index=dateindex, columns=columnNames)
    #print dataFrame
    #dataSeries = pd.Series(dataFrame)
    #print dataframe.head(), dataframe.columns
    print dataframe.describe() # gives info on count, mean, std dev, min/max, etc of columns
    #plt.show(dataframe.plot())
    #dfspc = dataframe.iloc[[5, 7, 14]]
    #print dfspc.columns
    #print tsdf



#pdt1("sample5 Attributes and Time Discrepencies t-0mins")
pdt1('sample5 Attributes and Time Discrepencies t-0mins')

# http://pandas.pydata.org/pandas-docs/stable/indexing.html