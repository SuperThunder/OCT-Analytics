import matplotlib.pyplot as plt
import pandas as pd

# todo: make plots sorted and labelled by proper datetime

def plotpoints(FILE_NAME, xlabel, ylabel, title, key):
    with open(FILE_NAME+'.csv', 'rb') as sample:
        data = pd.read_csv(sample, parse_dates=True, na_values=['-50','-100'])
        indexes = list(range(len(data)))  # Create a list of the indexes to use to graph the time series
        # Can potentially add a color spectrum to this
        plt.plot(indexes, data[key], marker='o', color='g', markeredgecolor='None', linewidth=0)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.show()


def plotlines(FILE_NAME, xlabel, ylabel, title, key):
    with open(FILE_NAME+'.csv', 'rb') as sample:
        data = pd.read_csv(sample, parse_dates=True, na_values=['-50','-100'])
        indexes = list(range(len(data)))  # Create a list of the indexes to use to graph the time series
        # Can potentially add a color spectrum to this
        plt.plot(indexes, data[key], marker='o', color='g', markeredgecolor='None', linewidth = 1)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.show()


# file names given in an array
def multiplotlines(FILE_NAMES, xlabel, ylabel, title, key):
    datasets = []
    colors = ['g', 'r', 'c', 'm', 'y', 'b', 'k']
    colind = 0
    for name in FILE_NAMES:
        file = open(name+'.csv', 'rb')
        data = pd.read_csv(file, parse_dates=True, na_values=['-50','-100'])
        indexes = list(range(len(data)))
        plt.plot(indexes, data[key], marker='o', color=colors[colind], markeredgecolor='None', linewidth = 1)
        colind += 1
        #datasets.append(plotdata(data, indexes))

    plt.show()


class plotdata:
    def __init__(self, data, indexes):
        self.data = data
        self.indexes = indexes
