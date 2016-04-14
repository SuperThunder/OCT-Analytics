import datetime
import csv

# Split data into as small attributes as possible and find difference between scheduled time and estimate at that time
def schVsEst(liveCSV, scheduleCSV):
    with open(liveCSV+'.csv','rb') as liveData:
        with open(scheduleCSV+'.csv','rb') as schData:
            with open('Attributes'+liveCSV+scheduleCSV, 'wb') as dest:
