import datetime

# Converts the datetime string to the hour of the day
def toHour(csvName):
    fileName = csvName + '.csv'
    newCSV = csvName + 'Hours' + '.csv'

    with open(fileName, 'rb') as source:
        with open(newCSV, 'wb') as dest:


