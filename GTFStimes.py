import csv

# Makes a single column csv of all the stop times, sorted by time
def makeTimesDB(csvName, stopID, route):
    outputName = csvName + stopID + 'Times'
    with open(csvName, 'rb') as source:
        with open('GTFSScheduledTimes'+stopID+'-'+route+'.csv', 'wb') as dest:
            csvReader = csv.reader(source)
            csvWriter = csv.writer(dest)


            #valList.append([])  # Can probably replace this with a list comprehension in the declaration
            #valList.append([])
            #valDict = {}
            #valDict
            tripList = []
            timeList = []
            for row in csvReader:
                if row[3] == stopID:
                    #print row[0], row[1]
                    csvRow = row[0], row[1]
                    tripList.append(row[0])  # Add the trip code
                    timeList.append(row[1])  # Add the scheduled time
                    csvWriter.writerow([row[0], row[1]])

                    #valList[0].append(row[0])
                    #valList[1].append(row[1])
                    #valList.append({row[0]: row[1]})
                    #addToDict(valDict, row[0], row[1])

            #print valDict

            #print sorted([tuple(map(int, d.split(":"))) for d in valList[1]])

# http://stackoverflow.com/questions/18817789/how-to-add-values-to-existing-dictionary-key-python
def addToDict(valDict, key, value):
    if key in valDict:
        valDict[key].update({key:value})
    else:
        valDict[key] = value


    #return valDict

makeTimesDB('./google_transit/stop_times.csv', 'AA060', '9')
