import matplotlib.pyplot as plt
import matplotlib.dates as mpldt
import pandas as pd
from math import isnan

# todo: make plots sorted and labelled by proper datetime
# http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.plot_date
# Above could be very helpful

def plotpoints(FILE_NAME, xlabel, ylabel, title, key):
    with open(FILE_NAME+'.csv', 'rb') as sample:
        data = pd.read_csv(sample, parse_dates=True, na_values=['-50','-100'])
        indexes = list(range(len(data)))  # Create a list of the indexes to use to graph the time series
        # Can potentially add a color spectrum to this
        plt.figure(figsize=(19.2, 10.8))
        plt.plot(indexes, data[key], marker='o', color='g', markeredgecolor='None', linewidth=0)
        plt.subplots_adjust(left=0.03, right=0.99, bottom=0.05, top=0.97)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        #plt.show()
        plt.savefig('./Plots/'+title+'Points plot'+'.png', format='png', dpi=100)
        plt.clf()



def plotline(FILE_NAME, xlabel, ylabel, title, key):
    with open(FILE_NAME+'.csv', 'rb') as sample:
        data = pd.read_csv(sample, parse_dates=True, na_values=['-50','-100'])
        indexes = list(range(len(data)))  # Create a list of the indexes to use to graph the time series
        # Can potentially add a color spectrum to this
        plt.plot(indexes, data[key], marker='o', color='g', markeredgecolor='None', linewidth=1)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        #plt.show()
        plt.savefig('./Plots/' + title + 'Line plot'+'.png', format='png', dpi=1000)
        plt.clf()


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
    plt.subplots_adjust(left=0.03, right = 0.99, bottom = 0.05, top = 0.97, figsize=(3, 2))
    plt.legend(title=legendtitle)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    #plt.show()
    plt.savefig('./Plots/' + title + 'Multiple line plot'+'.png', format='png', dpi=1000)
    plt.clf()


# Add each series/line of data to the same plot
# Probably need to either subplot the different days or fiddle with the mpl ticker to seperate the days
# Or potentially plot each day for each data set
# http://matplotlib.org/examples/api/date_demo.html
def multiplotlinesdt(FILE_NAMES, FILE_LABELS, xlabel, ylabel, title, legendtitle, key):
    # todo: make some kind of color system so more than 7 plots can be displayed
    colors = ['g', 'r', 'c', 'm', 'y', 'b', 'k']
    fileindex = 0
    filedays = [] # this is a list of datafile classes
    for name in FILE_NAMES:
        datasrc = open(name + '.csv', 'rb')
        data = pd.read_csv(datasrc, parse_dates=True, na_values=['-50', '-100', ''])
        # Want to make a t-_ list of the classes of daily lists of predicted discrepancies
        # so for every file (make a list of these as a list of datafile classes)
        # Then in each of those datafile classes have a weekdaydata class that will contain 23 predicted discrepancies
        # Graphing will then be done Day(subplot for mo-su)->each t-_ line data set graphed by x=1-23 y=prd dcr
        predictions = []
        currentpredictions = []
        for prd in data['Predicted Discrepancy']:
            if not isnan(prd):  # this is to deal with the blank lines between days
                currentpredictions.append(prd)
                #print prd
            else:  # the blank lines are actually handy to know when a new day of predictions is starting
                predictions.append(currentpredictions)
                #print currentpredictions
                currentpredictions = []
        #print len(predictions)
        weekdata = weekdaydata(predictions)
        fileday = datafile(FILE_LABELS[fileindex], weekdata)
        filedays.append(fileday)

        fileindex += 1

    print title, filedays
    # Plotting: For each subplot (of each day), plot each t-_ line for that day from 6:00 to 23:00
    # Each t-_ line can be accessed as filedays[weekday].data.<mon/tue/etc>
    fig, (mo, tu, we, th, fr, sa, su) = plt.subplots(sharex=False, sharey=False, figsize=(19.2, 10.8), nrows=1, ncols=7)
    axes = (mo, tu, we, th, fr, sa, su)
    index = 0
    xdata = list(range(6, 24))  # 6 AM to 11 PM
    for axis in axes:
        for i in range(0, len(FILE_NAMES)):
            ydata = filedays[i].data.weekdata[index]
            axis.plot(xdata, ydata, color=colors[i], markeredgecolor='None', linewidth=1,
                  label=FILE_LABELS[i], marker='o')

        index += 1

    #fig.show()
    plt.subplots_adjust(left=0.03, right=0.98, bottom=0.05, top=0.97)
    plt.legend(title=legendtitle)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    #plt.show()
    plt.savefig('./Plots/' + title + 'Datetime Multiple Lines plot'+'.png', format='png', dpi=100)
    plt.clf()


# This will generate a graph for each day of the week
def indplotlinesdt(FILE_NAMES, FILE_LABELS, xlabel, ylabel, title, legendtitle, key):
    # todo: make some kind of color system so more than 7 plots can be displayed
    colors = ['g', 'r', 'c', 'm', 'y', 'b', 'k']
    fileindex = 0
    filedays = [] # this is a list of datafile classes
    for name in FILE_NAMES:
        datasrc = open(name + '.csv', 'rb')
        data = pd.read_csv(datasrc, parse_dates=True, na_values=['-50', '-100', ''])
        # Want to make a t-_ list of the classes of daily lists of predicted discrepancies
        # so for every file (make a list of these as a list of datafile classes)
        # Then in each of those datafile classes have a weekdaydata class that will contain 23 predicted discrepancies
        # Graphing will then be done Day(subplot for mo-su)->each t-_ line data set graphed by x=1-23 y=prd dcr
        predictions = []
        currentpredictions = []
        for prd in data['Predicted Discrepancy']:
            if not isnan(prd):  # this is to deal with the blank lines between days
                currentpredictions.append(prd)
                #print prd
            else:  # the blank lines are actually handy to know when a new day of predictions is starting
                predictions.append(currentpredictions)
                #print currentpredictions
                currentpredictions = []
        #print len(predictions)
        weekdata = weekdaydata(predictions)
        fileday = datafile(FILE_LABELS[fileindex], weekdata)
        filedays.append(fileday)

        fileindex += 1

    print title, filedays
    # Plotting: For each subplot (of each day), plot each t-_ line for that day from 6:00 to 23:00
    # Each t-_ line can be accessed as filedays[weekday].data.<mon/tue/etc>
    fig, (mo, tu, we, th, fr, sa, su) = plt.subplots(7, sharex=False, sharey=False, figsize=(19.2, 10.8))
    axes = (mo, tu, we, th, fr, sa, su)
    index = 0
    xdata = list(range(6, 24))  # 6 AM to 11 PM
    for axis in axes:
        for i in range(0, len(FILE_NAMES)):
            ydata = filedays[i].data.weekdata[index]
            axis.plot(xdata, ydata, color=colors[i], markeredgecolor='None', linewidth=1,
                  label=FILE_LABELS[i])

        index += 1

    #fig.show()
    plt.subplots_adjust(left=0.03, right=0.90, bottom=0.05, top=0.97)
    plt.legend(title=legendtitle)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    #plt.show()
    plt.savefig('./Plots/' + title + 'Datetime Multiple Lines plot', format='png', dpi=100)
    plt.clf()




class datafile:
    def __init__(self, label, data): # data here is a weekdaydata class
        self.label = label
        self.data = data

class weekdaydata:
    def __init__(self, montosun):
        self.weekdata = montosun
        '''
        self.mon = montosun[0]
        self.tue = montosun[1]
        self.wed = montosun[2]
        ydata = filedays[index].data
        self.thu = montosun[3]
        self.fri = montosun[4]
        self.sat = montosun[5]
        self.sun = montosun[6]
        '''


class plotdata:
    def __init__(self, data, indexes):
        self.data = data
        self.indexes = indexes
