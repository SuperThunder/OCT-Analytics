import pandas as pd
import csv

def concsv(oldname, newname):

    allcols = ['StopNum','RouteNum','PollTime','TimeToNext','NextBusStartTime','TimeTo2nd','TimeTo3rd']
    outcols = ['StopNum', 'RouteNum', 'PollTime', 'TimeToNext']

    legacy = open(oldname+'.csv', 'rb')
    legacyreader = csv.reader(legacy)
    newlegacy = open(oldname + 'new.csv', 'wb')
    legacywriter = csv.writer(newlegacy)
    legacywriter.writerow(allcols)
    for row in legacyreader:
        legacywriter.writerow(row+ ['-50', '-50', '-50'])


    first = pd.read_csv(oldname+'new.csv', header=0)
    secnd = pd.read_csv(newname+'.csv', header=0)
    outpt = pd.concat(objs=[first, secnd])

    outpt.to_csv('currentdata.csv', index=False)
