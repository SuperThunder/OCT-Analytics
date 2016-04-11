import csv

# Makes a single column csv of all the stop times, sorted by time
def makeTimesDB(csvName, stopID, route):
    outputName = csvName + stopID + 'Times'
    with open(csvName, 'rb') as source:
        with open(outputName, 'wb') as dest:
            csvReader = csv.reader(source)
            csvWriter = csv.writer(dest)

            for row in csvReader:
                if row[3] == stopID:
                    print row[0], row[1]

                '''
                if i == 0:
                    print row
                i +=1
                '''

makeTimesDB('./google_transit/stop_times.csv', 'AA060', '9')