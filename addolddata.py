import csv

# Hooray for janky solutions that work
def concsv(oldname, newname, currentname):

    allcols = ['StopNum','RouteNum','PollTime','TimeToNext','NextBusStartTime','TimeTo2nd','TimeTo3rd']

    legacy = open(oldname+'.csv', 'rb')
    legacyreader = csv.reader(legacy)
    next(legacyreader, None)  # skip header of legacy data
    new = open(newname + '.csv', 'rb')
    newreader = csv.reader(new)
    next(newreader, None)
    output = open(currentname+'.csv', 'wb')
    outputwriter = csv.writer(output)
    outputwriter.writerow(allcols)  # Write the headers

    for row in legacyreader:
        outputwriter.writerow(row + ['-50', '-50', '-50']) # fill in error values for missing data

    for row in newreader:
        outputwriter.writerow(row)
