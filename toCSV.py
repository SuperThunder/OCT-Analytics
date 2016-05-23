# Takes the DB format used up until 2016-04-02 and converts the relevant values to CSV
# As it turns out it handles the new format fine too. I'm a better future-proofer than I thought

import sqlite3
import csv


def toCSV(dbName):
    dbFilename = dbName + '.db'
    dbConn = sqlite3.connect(dbFilename)

    csvName = dbName + '.csv'
    # Open file in write-only binary mode to ensure Windows doesn't interfere with writing
    with open(csvName, 'wb') as csvFile:
        csvWriter = csv.writer(csvFile)
        # This creates an iterable object where you can access the column values in a row by treating it as a tuple
        #dbCursor = dbConn.execute("SELECT PollTime, TimeToNext FROM Times WHERE TimeToNext > -1;")
        dbCursor = dbConn.execute("SELECT * FROM TIMES")  # Get everything from Times
        tableInfo = dbConn.execute("PRAGMA table_info(Times);")
        tableNames = tableInfo.fetchall()
        nameList = []
        for key in tableNames:
            nameList.append(key[1])  # 2nd value in table info is name

        # Write the column headers
        csvWriter.writerow(nameList)
        # Write the column values
        for row in dbCursor:
            csvWriter.writerow(row)

    dbConn.close()
