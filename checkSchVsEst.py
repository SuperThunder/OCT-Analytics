import datetime
import csv
from collections import defaultdict, OrderedDict

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
    exclDatesDict = genExclusionDays()
    exclDates = exclDatesDict.keys()
    print "Exclusion dates: ", exclDatesDict
    '''
    tripDatesDict = retServiceID_DateRanges()
    tripServiceIDs = tripDatesDict.keys()
    print 'Trip date ranges: ', tripDatesDict
    '''
    tripDates = retServiceID_DateRanges()
    print 'Trip date ranges: ', tripDates

    timeDiff = endDate - startDate  # This gives us a timedelta class result

    serviceIDDates = OrderedDict()  # Nice to have an ordered dict as it keeps earliest dates first
    expectedArrivals = []
    # todo: finish finding all scheduled times here
    with open(scheduleCSV+'.csv', 'rb') as schData:
        # Go through all the days we have live data for here
        for i in range(0, timeDiff.days+2):  # Account for two off by ones: timeDiff.days, and the range not being upper inclusive
            curDatetime = startDate + datetime.timedelta(days=i)  # Add days to our starting date
            curDatetimeStr = datetime.datetime.strftime(curDatetime, '%Y%m%d')
            # Check if the date is a special exclusion date defined by calendar_dates
            if curDatetimeStr in exclDates:
                serviceIDDates[curDatetimeStr] = exclDatesDict[curDatetimeStr]
            # Otherwise find the regular schedule ID
            else:
                for dr in tripDates:
                    if dr.start < curDatetime < dr.end:  # Check the date is within the range of the service ID
                        #print 'within range for', dr.serviceID, curDatetimeStr
                        if dr.weekdays[curDatetime.weekday()] == '1':  # Then check it is the right day of the week
                            #print 'match for ', dr.serviceID
                            serviceIDDates[curDatetimeStr] = dr.serviceID
                '''
                for val in tripDatesDict.itervalues():
                    print ''
                for key in tripServiceIDs:
                    print key, tripDatesDict
                    serv = list(tripDatesDict[key])

                    if serv[7] < curDatetime < serv[8]:
                        print ''
                '''

        print 'Service IDs: ', serviceIDDates




def genExclusionDays():
    with open('./google_transit/calendar_dates.txt', 'rb') as exclDates:
        exclDatesCSV = csv.reader(exclDates)
        #exclDatesDicts = []
        exclDatesDict = defaultdict(list)
        next(exclDatesCSV, None)  # skip header
        for row in exclDatesCSV:
            if row[2] == '2':  # Check that the exception type is service added and not removed
                exclDatesDict[row[1]].append(row[0])

    return exclDatesDict

# Hardcoded for specific busses, won't work with everything
def retServiceID_DateRanges():
    with open('./google_transit/calendar.txt', 'rb') as trips:
        calendarCSV = csv.reader(trips)
        calendarDates = defaultdict(list)
        calendarRanges = []
        next(calendarCSV, None)  # skip header
        # luckily only need first 6 rows of data for the 9 schedule. this is the hardcoded part.
        i = 0
        for row in calendarCSV:
            if i < 6:
                daterange = serviceIDDateRange(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                                               datetime.datetime.strptime(row[8], '%Y%m%d'),
                                               datetime.datetime.strptime(row[9], '%Y%m%d'))
                calendarRanges.append(daterange)
                '''
                calendarDates[row[0]].append([row[1], row[2], row[3], row[4], row[5],
                                          row[6], row[7], datetime.datetime.strptime(row[8], '%Y%m%d'),
                                          datetime.datetime.strptime(row[9], '%Y%m%d')])
                '''
            i += 1

    return calendarRanges

# Class that is much saner to use for service range information than a dictionary
class serviceIDDateRange:
    def __init__(self, serviceID, mon, tue, wed, thu, fri, sat, sun, start, end):
        self.serviceID = serviceID
        self.weekdays = [mon, tue, wed, thu, fri, sat, sun]
        self.start = start
        self.end = end


'''
def checkIfExclDay(day, exclDays):
    for days in exclDays:
        if day == days:
'''

schVsEst('sample2.dbCSV', 'GTFSScheduledTimesAA060-9')