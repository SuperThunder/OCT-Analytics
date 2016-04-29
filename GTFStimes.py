import csv
import datetime
import operator


# Makes a single column csv of all the stop times, sorted by time
def getStopSchInfo(csvName, stopID, route):

    outputName = 'GTFSScheduledTimes'+stopID+'-'+route+'.csv'

    print 'Opening CSVs'

    valList = []

    with open(csvName, 'rb') as source:
        with open(outputName, 'wb') as dest:
            csvReader = csv.reader(source)
            csvWriter = csv.writer(dest)
            csvWriter.writerow(['Service ID', 'Trip', 'Time'])  # Write the column headers

            for row in csvReader:
                if row[3] == stopID:
                    schTime = datetime.datetime.strptime(row[1], '%H:%M:%S')
                    newTime = datetime.datetime.strftime(schTime, '%H%M%S')

                    # Need to split the tripID into its trip number and calendar code parts
                    trip, serviceID = splitTripID(row[0])

                    valList.append((serviceID, trip, newTime))

            # Sort by Calendar code then time to get all the times of each group in order
            valList.sort(key=operator.itemgetter(0, 2))

            for item in valList:
                csvWriter.writerow(item)

    print "Scraping complete"


def splitTripID(tripID):
    ind = tripID.find('-')
    trip = ''
    serviceID = ''
    for i in range(0, ind):
        trip += tripID[i]

    for i in range(ind+1, len(tripID)):
        serviceID += tripID[i]

    return trip, serviceID

