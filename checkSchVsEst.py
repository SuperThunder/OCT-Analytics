import datetime
import csv

# Split data into as small attributes as possible and find difference between scheduled time and estimate at that time
def schVsEst(liveCSV, scheduleCSV):

    with open(liveCSV+'.csv', 'rb') as liveData:
        with open(scheduleCSV+'.csv', 'rb') as schData:
            with open('Attributes of '+liveCSV+scheduleCSV+'.csv', 'wb') as dest:
                csvLiveReader = csv.reader(liveData)
                csvSchReader = csv.reader(schData)
                csvOutput = csv.writer(dest)
                headerRow = ['StopNum', 'RouteNum', 'PollTimeYear', 'PollTimeMonth', 'PollTimeMonthNum',
                             'PollTimeWeekday', 'PollTimeDay', 'PollTimeHour', 'PollTimeMinute', 'PollTimeSecond',
                             'TimeToNext', 'TimeTo2nd']
                # 'GTFSServiceID', 'SchTime', 'TimeDiff']
                csvOutput.writerow(headerRow)
                splitIntoAttributes(csvLiveReader, csvOutput)




def splitIntoAttributes(liveData, liveAttribData):

    next(liveData, None)  # Skip header row
    for row in liveData:
        # ex: Thu Mar 24 22:16:00 2016

        timeObj = datetime.datetime.strptime(row[2], '%a %b %d %H:%M:%S %Y')

        monthNames = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep',
                      10: 'Oct', 11: 'Nov', 12: 'Dec'}
        # todo: doesn't write in weekday properly
        attribRow = [row[0], row[1], timeObj.year, monthNames[timeObj.month], timeObj.month, timeObj.weekday, timeObj.day,
                   timeObj.hour, timeObj.minute, timeObj.second, row[3], row[4]]
        liveAttribData.writerow(attribRow)

schVsEst('sample2.dbCSV', 'GTFSScheduledTimesAA060-9')