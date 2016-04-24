import csv

timeswint = open('./google_transit_winter/stop_times.txt', 'rb')
timesapr = open('./google_transit_april22onwards/stop_times.txt', 'rb')
timescombined = open('./google_transit_combined/stop_times.txt', 'wb')

wintCSV = csv.reader(timeswint)
aprCSV = csv.reader(timesapr)
combCSV = csv.writer(timescombined)

allrows = []

for row in aprCSV:
    allrows.append(row)

for row in wintCSV:
    allrows.append(row)

print 'writing new csv'
for row in allrows:
    combCSV.writerow(row)
