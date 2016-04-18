import datetime
import csv

# Split data into as small attributes as possible and find difference between scheduled time and estimate at that time
def schVsEst(liveCSV, scheduleCSV):
    with open(liveCSV+'.csv', 'rb') as liveData:
        with open(scheduleCSV+'.csv', 'rb') as schData:
            with open('Attributes'+liveCSV+scheduleCSV+'.csv', 'wb') as dest:
                csvLiveReader = csv.reader(liveData)
                csvSchReader = csv.reader(schData)
                csvOutput = csv.writer(dest)
                headerRow = ['StopNum', 'RouteNum', 'PollTimeYear', 'PollTimeMonth', 'PollTimeMonthNum',
                             'PollTimeWeekday', 'PolLTimeDay', 'PolLTimeHour', 'PollTimeMinute', 'PollTimeSecond',
                             'TimeToNext', 'TimeTo2nd' 'GTFSTrip', 'GTFSServiceID', 'SchTime', 'TimeDiff']
                csvOutput.writeline(headerRow)

                destRow = []
                #get first and last date in live data?


schVsEst('sample2.dbCSV', 'GTFSScheduledTimesAA060-9')