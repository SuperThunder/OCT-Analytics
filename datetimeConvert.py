import datetime
import pandas as pd

# Converts the datetime string to a different format
def toHour(csvName, dtFormat):
    oldCSV = csvName + '.csv'
    newCSV = csvName + 'Hours' + '.csv'
    if dtFormat == 'def':
        dtFormat = "%Y%m%d%H%M%S"

    # Open the source CSV and also parse all the datetimes in column 3 (PollTime)
    source = pd.read_csv(oldCSV, parse_dates=[2])
    # Writes the CSV to a new file with the datetimes in a different format
    source.to_csv(newCSV, mode='wb', date_format=dtFormat)

toHour("sample2.dbCSV", "%H")
