import datetime
import csv
from collections import defaultdict, OrderedDict

# todo: create a logfile to deal with all the console output
# Split data into as small attributes as possible and find difference between scheduled time and estimate at that time
def schVsEst(liveCSV, scheduleCSV, minsBeforeArrival):

    attribFileName = 'Attributes of '+liveCSV+'.csv'
    # Split poll times of live data into specific attributes
    with open(liveCSV+'CSV.csv', 'rb') as liveData:
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
    '''
    for arrival in scheduledTimes:
        print arrival.day
    '''

    liveTimes = []
    # Find the discrepancy of scheduled and live times
    with open('Attributes of '+liveCSV+'.csv', 'rb') as attribs:
        csvAttribReader = csv.reader(attribs)
        next(csvAttribReader, None)
        for row in csvAttribReader:
            liveTimes.append(liveEstimates(stopnum=row[0], routenum=row[1], polltime=row[12],
                                           timetonext=row[10], timeto2nd=row[11]))
    with open('Attributes and Time Discrepencies'+liveCSV+'t-'+str(minsBeforeArrival)+'mins.csv', 'wb') as discr:
        csvDiscrWriter = csv.writer(discr)
        csvDiscrWriter.writerow(['StopNum', 'RouteNum', 'PollTimeYear', 'PollTimeMonth', 'PollTimeMonthNum',
                         'PollTimeWeekday', 'PollTimeDay', 'PollTimeHour', 'PollTimeMinute', 'PollTimeSecond',
                         'TimeToNext', 'TimeTo2nd', 'FullPollTime', 'ScheduledTime', 'Discrepancy'])
        #print scheduledTimes
        # need to iterate through the scheduled times in the time for which we have live times
        monthNames = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep',
                      10: 'Oct', 11: 'Nov', 12: 'Dec'}

        # todo: this is really really slow. set up the live times so they can be found by day. ordered dict?
        print 'matching scheduled times to estimates'
        for day in scheduledTimes:
            for arrival in day.arrivals:
                arrivalTime = datetime.datetime.strptime(day.day+arrival, '%Y%m%d%H%M%S')
                arrivalTime += datetime.timedelta(minutes=-1*minsBeforeArrival)
                for timeEst in liveTimes:
                    if datetime.datetime.strptime(timeEst.PollTime, '%a %b %d %H:%M:%S %Y') == arrivalTime:
                        print timeEst.PollTime, timeEst.TimeToNext
                        timeObj = datetime.datetime.strptime(timeEst.PollTime, '%a %b %d %H:%M:%S %Y')
                        row = [timeEst.StopNum, timeEst.RouteNum, timeObj.year, monthNames[timeObj.month],
                               timeObj.month, timeObj.isoweekday(), timeObj.day, timeObj.hour, timeObj.minute,
                               timeObj.second, timeEst.TimeToNext, timeEst.TimeTo2nd, timeEst.PollTime,
                               arrival]
                        csvDiscrWriter.writerow(row)
        print 'done'


def splitIntoAttributes(liveData, liveAttribData):
    next(liveData, None)  # Skip header row
    for row in liveData:
        # ex: Thu Mar 24 22:16:00 2016

        timeObj = datetime.datetime.strptime(row[2], '%a %b %d %H:%M:%S %Y')

        monthNames = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep',
                      10: 'Oct', 11: 'Nov', 12: 'Dec'}
        # note: getting the weekday is an instance method, everything else is a object class attribute
        attribRow = [row[0], row[1], timeObj.year, monthNames[timeObj.month], timeObj.month, timeObj.isoweekday(),
                     timeObj.day, timeObj.hour, timeObj.minute, timeObj.second, row[3], row[5], row[2]]
        liveAttribData.writerow(attribRow)
        # todo: chance row[4] back to row[5] when not dealing with legacy data


# need to iterate through the scheduled times in the time for which we have live times
# return them as a dictionary of a date to its scheduled times
def getScheduledTimes(startDate, endDate, scheduleCSV):
    exclDatesDict = genExclusionDays()
    print "Exclusion dates: ", exclDatesDict
    tripDates = retServiceID_DateRanges()
    print 'Trip date ranges: ',
    for date in tripDates:
        print date.start, date.end, date.serviceID, '  ',
    print ''

    serviceIDDates = matchDateToID(exclDatesDict, tripDates, startDate, endDate)
    print 'Service IDs: ', serviceIDDates
    allArrivals = []
    serviceIDTimes = []  # Contains a list of a service ID class matched to its daily arrival times
    # Matches service IDs to their daily arrival times
    with open(scheduleCSV+'.csv', 'rb') as schData:
        schDataCSV = csv.reader(schData)
        next(schDataCSV, None)
        curID = ''
        numIDAdded = -1
        for row in schDataCSV:
            if curID == row[0]:
                # Some of the stop times are duplicated, so avoid adding duplicate times here
                # Ideally the stop times combined file just wouldn't be duplicated in places
                if serviceIDTimes[numIDAdded].arrivals[len(serviceIDTimes[numIDAdded].arrivals)-1] != row[2]:
                    serviceIDTimes[numIDAdded].arrivals.append(row[2])
                #print serviceIDTimes[numIDAdded].arrivals
            else:
                curID = row[0]
                numIDAdded += 1
                arrivalObj = IDArrivals(arrivals=[row[2]], serviceID=row[0])
                serviceIDTimes.append(arrivalObj)

    # Go through every date recorded with its service ID and get the arrival times for that service ID
    # todo: find out why april 17,22,23 don't get IDs to be matched here. they're all upper bounds to a date range
    print 'serviceIDDates: ', serviceIDDates
    for date in serviceIDDates:
        for arrivals in serviceIDTimes:
            if serviceIDDates[date] == arrivals.serviceID:
                print 'matched ', date, ' to ', arrivals.serviceID
                allArrivals.append(dailyArrivals(date, serviceIDDates[date], arrivals.arrivals))
                #print date, serviceIDDates[date], arrivals.arrivals
            else:
                #print 'was not able to match date', date, 'with serviceID', serviceIDDates[date]
                pass

    # Display all arrivals
    print 'Days and their arrival times: '
    for days in allArrivals:
        print days.day, days.arrivals

    writeScheduledArrivalstoCSV(allArrivals, startDate, endDate)
    return allArrivals


def genExclusionDays():
    with open('./google_transit_combined/calendar_dates.txt', 'rb') as exclDates:
        exclDatesCSV = csv.reader(exclDates)
        exclDatesDict = defaultdict(str)
        next(exclDatesCSV, None)  # skip header
        for row in exclDatesCSV:
            if row[2] == '2':  # Check that the exception type is service added and not removed
                exclDatesDict[row[1]] = row[0]

    return exclDatesDict


# Hardcoded for specific busses, won't work with everything
def retServiceID_DateRanges():
    with open('./google_transit_combined/calendar.txt', 'rb') as trips:
        calendarCSV = csv.reader(trips)
        calendarRanges = []
        next(calendarCSV, None)  # skip header
        # luckily only need first 6 rows of data for the 9 schedule. this is the hardcoded part.
        # Otherwise we would have to somehow know the service ID of our trip in advance
        #i = 0
        for row in calendarCSV:
            #if i < 6:
            daterange = serviceIDDateRange(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                                               datetime.datetime.strptime(row[8], '%Y%m%d'),
                                               datetime.datetime.strptime(row[9], '%Y%m%d'))
            calendarRanges.append(daterange)
            #i += 1

    return calendarRanges


# Matches each date to its appropriate service ID by checking whether it is an exclusion date or a normal day
def matchDateToID(exclDatesDict, tripDates, startDate, endDate):
    exclDates = exclDatesDict.keys()
    timeDiff = endDate - startDate  # This gives us a timedelta class result
    serviceIDDates = OrderedDict()  # Nice to have an ordered dict as it keeps earliest dates first
    # Go through all the days we have live data for here
    for i in range(0, timeDiff.days+1):
        curDatetime = startDate + datetime.timedelta(days=i)  # Add days to our starting date
        curDatetimeStr = datetime.datetime.strftime(curDatetime, '%Y%m%d')
        # Check if the date is a special exclusion date defined by calendar_dates
        if curDatetimeStr in exclDates:
            serviceIDDates[curDatetimeStr] = exclDatesDict[curDatetimeStr]
        # Otherwise find the regular schedule ID
        else:
            for dr in tripDates:  # go through all the date ranges of the service IDs
                oneday = datetime.timedelta(days=1)

                ''' not totally sure how reliably the system will handle dates past the 22nd of april
                if curDatetime > datetime.datetime.strptime('201604222359', '%Y%m%d%H%M'):
                    print 'Date out of range of old schedule', curDatetime
                '''
                # Without subtracting or adding enough time the program won't match the start/end days to their proper IDs
                # this is what subtracting/adding oneday is for
                if dr.start-oneday < curDatetime < dr.end+oneday:  # Check the date is within the range of the service ID
                    #print 'within range for', dr.serviceID, curDatetimeStr
                    if dr.weekdays[curDatetime.weekday()] == '1':  # Then check it is the right day of the week
                        #print 'match for ', dr.serviceID
                        serviceIDDates[curDatetimeStr] = dr.serviceID
    return serviceIDDates


# Writes all the scheduled times found in the date range to CSV
def writeScheduledArrivalstoCSV(allArrivals, startDate, endDate):
    startDateStr = datetime.datetime.strftime(startDate, '%Y%m%d')
    endDateStr = datetime.datetime.strftime(endDate, '%Y%m%d')
    csvName = 'ScheduledArrivals'+startDateStr+'to'+endDateStr+'.csv'
    with open(csvName, 'wb') as dest:
        csvWriter = csv.writer(dest)
        csvWriter.writerow(['Day', 'ServiceID', 'Arrivals'])
        for day in allArrivals:
            for arrival in day.arrivals:
                csvWriter.writerow([day.day, day.serviceID, arrival])
    print 'All scheduled times written to CSV ', csvName


# Class that is much saner to use for service range information than a dictionary
class serviceIDDateRange:
    def __init__(self, serviceID, mon, tue, wed, thu, fri, sat, sun, start, end):
        self.serviceID = serviceID
        self.weekdays = [mon, tue, wed, thu, fri, sat, sun]
        self.start = start
        self.end = end

class IDArrivals:
    def __init__(self, serviceID, arrivals):
        self.serviceID = serviceID
        self.arrivals = arrivals

class dailyArrivals:
        def __init__(self, day, serviceID, arrivals):
            self.day = day
            self.serviceID = serviceID
            self.arrivals = arrivals

class liveEstimates:
    def __init__(self, stopnum, routenum, polltime, timetonext, timeto2nd):
        self.StopNum = stopnum  # OC Transpo stop number
        self.RouteNum = routenum  # OC Transpo bus route number
        self.PollTime = polltime  # the date and time at which the API call was made
        self.TimeToNext = timetonext  # the estimated time to the next bus arrival at StopNum of the RouteNum bus
        self.TimeTo2nd = timeto2nd  # the estimated time to the 2nd next bus

# run instructions: sample live data csv name, source for stoptimes CSV, number of minutes before the scheduled arrival
# that the estimated times should be checked
schVsEst('sample5', 'GTFSScheduledTimesAA060-9', 1)