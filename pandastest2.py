import matplotlib.pyplot as plt
import pandas as pd

def plottest(FILE_NAME, xlabel, ylabel, title, key):
    with open(FILE_NAME, 'rb') as sample:
        data = pd.read_csv(sample, parse_dates=True, na_values=['-50','-100'])
        indexes = list(range(len(data)))  # Create a list of the indexes to use to graph the time series
        # Can potentially add a color spectrum to this
        plt.plot(indexes, data[key], marker='o', color='g', markeredgecolor='None')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.show()

plottest('sample5CSV.csv', 'Index', 'TimeToNext', 'Index vs TimeToNext', 'TimeToNext')
plottest('./Machine learning results/SVR Predictions for sample5 Attributes and Time Discrepencies t-1mins.csv',
         'Index', 'Expected Discrepancy', 'Predicted Discrepancy vs Weekdays', 'Predicted Discrepancy')