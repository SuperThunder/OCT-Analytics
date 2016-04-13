import csv
import datetime
import operator


# Makes a single column csv of all the stop times, sorted by time
def makeTimesDB(csvName, stopID, route):

    outputName = 'GTFSScheduledTimes'+stopID+'-'+route+'.csv'

    print 'Opening CSVs'

    #valList = [('Trip', 'Service ID', 'Time')]
    valList = []

    with open(csvName, 'rb') as source:
        with open(outputName, 'wb') as dest:
            csvReader = csv.reader(source)
            csvWriter = csv.writer(dest)
            csvWriter.writerow(['Trip', 'Service ID', 'Time'])  # Write the column headers

            for row in csvReader:
                if row[3] == stopID:
                    schTime = datetime.datetime.strptime(row[1], '%H:%M:%S')
                    newTime = datetime.datetime.strftime(schTime, '%H%M%S')

                    # Need to split the tripID into its trip number and calendar code parts
                    trip, serviceID = splitTripID(row[0])

                    valList.append((serviceID, trip, newTime))

                    #csvWriter.writerow([serviceID, trip, newTime])

            valList.sort(key=operator.itemgetter(0))
            valList.sort(key=operator.itemgetter(2))

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

# http://stackoverflow.com/questions/18817789/how-to-add-values-to-existing-dictionary-key-python
def addToDict(valDict, key, value):
    if key in valDict:
        valDict[key].update({key:value})
    else:
        valDict[key] = value


    #return valDict

makeTimesDB('./google_transit/stop_times.csv', 'AA060', '9')
