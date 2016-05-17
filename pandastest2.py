import matplotlib.pyplot as plt
import matplotlib.dates as mpldt
import pandas as pd
from collections import defaultdict

# todo: make plots sorted and labelled by proper datetime
# http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.plot_date
# Above could be very helpful

def plotpoints(FILE_NAME, xlabel, ylabel, title, key):
    with open(FILE_NAME+'.csv', 'rb') as sample:
        data = pd.read_csv(sample, parse_dates=True, na_values=['-50','-100'])
        indexes = list(range(len(data)))  # Create a list of the indexes to use to graph the time series
        # Can potentially add a color spectrum to this
        plt.plot(indexes, data[key], marker='o', color='g', markeredgecolor='None', linewidth=0)
        plt.subplots_adjust(left=0.03, right=0.99, bottom=0.05, top=0.97)
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
def multiplotlines(FILE_NAMES, FILE_LABELS, xlabel, ylabel, title, legendtitle, key):
    # todo: make some kind of color system so more than 7 plots can be displayed
    colors = ['g', 'r', 'c', 'm', 'y', 'b', 'k']
    index = 0
    # Add each series/line of data to the same plot
    for name in FILE_NAMES:
        file = open(name+'.csv', 'rb')
        data = pd.read_csv(file, parse_dates=True, na_values=['-50','-100'])
        indexes = list(range(len(data)))
        plt.plot(indexes, data[key], marker='o', color=colors[index], markeredgecolor='None', linewidth = 1,
                 label=FILE_LABELS[index])
        index += 1

    # The subplot adjusting
    plt.subplots_adjust(left=0.03, right = 0.99, bottom = 0.05, top = 0.97)
    plt.legend(title=legendtitle)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


# Add each series/line of data to the same plot
# Probably need to either subplot the different days or fiddle with the mpl ticker to seperate the days
# Or potentially plot each day for each data set
# http://matplotlib.org/examples/api/date_demo.html
def multiplotlinesdt(FILE_NAMES, FILE_LABELS, xlabel, ylabel, title, legendtitle, key):
    # todo: make some kind of color system so more than 7 plots can be displayed
    colors = ['g', 'r', 'c', 'm', 'y', 'b', 'k']
    fileindex = 0
    filedays = []
    for name in FILE_NAMES:
        file = open(name + '.csv', 'rb')
        data = pd.read_csv(file, parse_dates=True, na_values=['-50', '-100', ''])
        # Want to make a t-_ list of the classes of daily lists of predicted discrepancies
        filedays[fileindex].append([])



class datafile:
    def __init__(self, label, data): # data here is a weekdaydata class
        self.label = label
        self.data = data

class weekdaydata:
    def __init__(self, mo, tu, we, th, fr, sa, su):
        self.mon = mo
        self.tue = tu
        self.wed = we
        self.thu = th
        self.fri = fr
        self.sat = sa
        self.sun = su


class plotdata:
    def __init__(self, data, indexes):
        self.data = data
        self.indexes = indexes
