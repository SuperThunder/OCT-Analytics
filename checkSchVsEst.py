import datetime
import csv
from collections import defaultdict

# Split data into as small attributes as possible and find difference between scheduled time and estimate at that time
def schVsEst(liveCSV, scheduleCSV):

    attribFileName = 'Attributes of '+liveCSV+'.csv'
    # Split poll times of live data into specific attributes
    with open(liveCSV+'.csv', 'rb') as liveData:
            with open(attribFileName, 'wb') as attribs:
                csvLiveReader = csv.reader(liveData)
                csvAttribWriter = csv.writer(attribs)
                headerRow = ['StopNum', 'RouteNum', 'PollTimeYear', 'PollTimeMonth', 'PollTimeMonthNum',
                             'PollTimeWeekday', 'PollTimeDay', 'PollTimeHour', 'PollTimeMinute', 'PollTimeSecond',
                             'TimeToNext', 'TimeTo2nd', 'FullPollTime']
                # 'GTFSServiceID', 'SchTime', 'TimeDiff']
                csvAttribWriter.writerow(headerRow)
                splitIntoAttributes(csvLiveReader, csvAttribWriter)

    # Get the start and end datetimes of our live data range
    with open(attribFileName, 'rb') as attribs:
        csvAttribReader = csv.reader(attribs)

        # get first row by skipping header
        next(csvAttribReader, None)
        firstAttribRow = csvAttribReader.next()
        for row in csvAttribReader:
            curRow = row

        lastAttribRow = curRow  # last value assigned to curRow will have been the last row of the CSV
        print 'Start row: ', firstAttribRow
        startDatetime = datetime.datetime.strptime(firstAttribRow[12], '%a %b %d %H:%M:%S %Y')
        print 'End row: ', lastAttribRow
        endDatetime = datetime.datetime.strptime(lastAttribRow[12], '%a %b %d %H:%M:%S %Y')

    scheduledTimes = getScheduledTimes(startDatetime, endDatetime, scheduleCSV)

    # Find the discrepancy of scheduled and live times
    with open('Attributes of '+liveCSV+'.csv', 'rb') as attribs:
            with open('Attributes and Time Discrepencies.csv', 'wb') as descr:
                csvAttribReader = csv.reader(attribs)
                csvDescrWriter = csv.writer(descr)
                # need to iterate through the scheduled times in the time for which we have live times



def splitIntoAttributes(liveData, liveAttribData):
    next(liveData, None)  # Skip header row
    for row in liveData:
        # ex: Thu Mar 24 22:16:00 2016

        timeObj = datetime.datetime.strptime(row[2], '%a %b %d %H:%M:%S %Y')

        monthNames = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep',
                      10: 'Oct', 11: 'Nov', 12: 'Dec'}
        # note: getting the weekday is an instance method, everything else is a object class attribute
        attribRow = [row[0], row[1], timeObj.year, monthNames[timeObj.month], timeObj.month, timeObj.isoweekday(),
                     timeObj.day, timeObj.hour, timeObj.minute, timeObj.second, row[3], row[4], row[2]]
        liveAttribData.writerow(attribRow)


# need to iterate through the scheduled times in the time for which we have live times
# return them as a dictionary of a date to its scheduled times
def getScheduledTimes(startDate, endDate, scheduleCSV):
    exclDates = genExclusionDays()
    print "Exclusion dates: ", exclDates
    tripDates = retServiceID_DateRanges()
    print 'Trip date ranges: ', tripDates

    timeDiff = endDate - startDate  # This gives us a timedelta class result

    # todo: finish finding all scheduled times here
    with open(scheduleCSV+'.csv', 'rb') as schData:
        # Go through all the days we have live data for here
        for i in range(0, timeDiff.days+2):  # Account for two off by ones: timeDiff.days, and the range not being upper inclusive
            curDatetime = startDate + datetime.timedelta(days=i)
            print curDatetime


        print ''

def genExclusionDays():
    with open('./google_transit/calendar_dates.txt', 'rb') as exclDates:
        exclDatesCSV = csv.reader(exclDates)
        #exclDatesDicts = []
        exclDatesDict = defaultdict(list)
        next(exclDatesCSV, None)  # skip header
        for row in exclDatesCSV:
            exclDatesDict[row[0]].append(row[1])

    return exclDatesDict

# Hardcoded for specific busses, won't work with everything
def retServiceID_DateRanges():
    with open('./google_transit/calendar.txt', 'rb') as trips:
        tripsCSV = csv.reader(trips)
        tripDates = defaultdict(list)
        next(tripsCSV, None)  # skip header
        # luckily only need first 6 rows of data for the 9 schedule. this is the hardcoded part.
        i = 0
        for row in tripsCSV:
            if i < 6:
                tripDates[row[0]].append([bool(row[1]), bool(row[2]), bool(row[3]), bool(row[4]), bool(row[5]),
                                          bool(row[6]), bool(row[7]), datetime.datetime.strptime(row[8], '%Y%M%d'),
                                          datetime.datetime.strptime(row[9], '%Y%M%d')])
            i += 1

    return tripDates

'''
def checkIfExclDay(day, exclDays):
    for days in exclDays:
        if day == days:
'''

schVsEst('sample2.dbCSV', 'GTFSScheduledTimesAA060-9')