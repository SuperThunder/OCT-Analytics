import csv

# Makes a single column csv of all the stop times, sorted by time
def makeTimesDB(csvName, stopID, route):
    outputName = csvName + stopID + 'Times'
    with open(csvName, 'rb') as source:
        with open('GTFSScheduledTimes'+stopID+'-'+route+'.csv', 'wb') as dest:
            csvReader = csv.reader(source)
            csvWriter = csv.writer(dest)

            valList = []
            valList.append([])  # Can probably replace this with a list comprehension in the declaration
            valList.append([])
            tripList = []
            timeList = []
            for row in csvReader:
                if row[3] == stopID:
                    #print row[0], row[1]
                    #tripList.append(row[0])  # Add the trip code
                    #timeList.append(row[1])  # Add the scheduled time
                    valList[0].append(row[0])
                    valList[1].append(row[1])

            print sorted([tuple(map(int, d.split(":"))) for d in valList[1]])


makeTimesDB('./google_transit/stop_times.csv', 'AA060', '9')