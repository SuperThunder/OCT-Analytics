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

# http://matplotlib.org/examples/api/date_demo.html
def multiplotlinesdt(FILE_NAMES, FILE_LABELS, xlabel, ylabel, title, legendtitle, key):
    datasets = []
    # todo: make some kind of color system so more than 7 plots can be displayed
    colors = ['g', 'r', 'c', 'm', 'y', 'b', 'k']
    index = 0

    years = mpldt.YearLocator()  # every year
    months = mpldt.MonthLocator()  # every month
    yearsFmt = mpldt.DateFormatter('%Y')

    # Add each series/line of data to the same plot
    # Probably need to either subplot the different days or fiddle with the mpl ticker to seperate the days
    for name in FILE_NAMES:
        file = open(name+'.csv', 'rb')
        data = pd.read_csv(file, parse_dates=True, na_values=['-50','-100', ''])
        indexes = list(range(len(data)))
        datetimes = []
        lastdt = '000' # part of the really bad solution
        for dt in data['Datetime']:
            print dt
            # The data has an empty row after the end of every row to make it more human readable
            # Unfortunately this means this null row has to be disregarded for conversion
            # but still added back to make dimensions fit
            if str(lastdt)[-2:] != '23':
                dtobj = pd.datetime.strptime(str(dt), '%A %H')
                datetimes.append(dtobj)
                #datetimes.append(mpldt.date2num(dtobj)) # Converting to a ticker doesn't take weekday into account
                #print datetimes[len(datetimes)-1]
            else:
                datetimes.append('')
            lastdt = dt
        print len(datetimes), datetimes
        print len(data[key])

        plt.plot(datetimes, data[key], marker='o', color=colors[index], markeredgecolor='None', linewidth = 1,
                 label=FILE_LABELS[index])
        #plt.plot_date(x=datetimes, y=data[key], fmt='%w %H')
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
