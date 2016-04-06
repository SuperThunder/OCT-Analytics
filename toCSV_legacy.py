# Takes the DB format used up until 2016-04-02 and converts the relevant values to CSV

import sqlite3
import csv
import datetime


def toCSV(dbName):
    dbName += '.db'
    dbConn = sqlite3.connect(dbName)
    #curs = dbConn.cursor()

    csvName = dbName + 'CSV.csv'
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


        #colNameList = [tuple[0] for keys in dbCursor.description]
        #print colNameList
        csvWriter.writerow(nameList)
        for row in dbCursor:
            #print tuple(row)
            csvWriter.writerow(row)

    dbConn.close()
