import matplotlib.pyplot as plt
import matplotlib.dates as mpldt
import pandas as pd

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
    datasets = []
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
        #datasets.append(plotdata
    # The subplot adjusting
    plt.subplots_adjust(left=0.03, right = 0.99, bottom = 0.05, top = 0.97)
    plt.legend(title=legendtitle)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


def multiplotlinesdt(FILE_NAMES, FILE_LABELS, xlabel, ylabel, title, legendtitle, key):
    datasets = []
    # todo: make some kind of color system so more than 7 plots can be displayed
    colors = ['g', 'r', 'c', 'm', 'y', 'b', 'k']
    index = 0
    # Add each series/line of data to the same plot
    for name in FILE_NAMES:
        file = open(name+'.csv', 'rb')
        data = pd.read_csv(file, parse_dates=True, na_values=['-50','-100', ''])
        indexes = list(range(len(data)))
        datetimes = []
        for dt in data['Datetime']:
            print dt
            if dt != '':
                datetimes.append(pd.datetime.strptime(str(dt), '%w %H'))  # 0 6:00
        print datetimes

        plt.plot(datetimes, data[key], marker='o', color=colors[index], markeredgecolor='None', linewidth = 1,
                 label=FILE_LABELS[index])
        index += 1
        #datasets.append(plotdata
    # The subplot adjusting
    plt.subplots_adjust(left=0.03, right = 0.99, bottom = 0.05, top = 0.97)
    plt.legend(title=legendtitle)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


class plotdata:
    def __init__(self, data, indexes):
        self.data = data
        self.indexes = indexes
