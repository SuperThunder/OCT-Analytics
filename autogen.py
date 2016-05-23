# Automate the generation of the files wanted for analysis by running their scripts
# Note that this can take some time, especially for the schedule vs estimate stage
# todo: combine the latest sample database with the legacy data for a wider data range
import toCSV
import GTFStimes
import checkSchVsEst
import addolddata

CURRENT_NAME = 'currentsample'
LEGACY_NAME = 'legacydata'
# If integration with legacy data causes any issues, simply change the sample name back to currentsampleCSV
SAMPLE_NAME = 'currentdata'

toCSV.toCSV(LEGACY_NAME)
toCSV.toCSV(CURRENT_NAME)

addolddata.concsv(LEGACY_NAME, CURRENT_NAME)


GTFStimes.getStopSchInfo('./google_transit_combined/stop_times.txt', 'AA060', '9')
# generate the estimated time discrepancy for up to 5 minutes before a schedule stop
for i in range(0, 6):
    print 'Finding discrepancies for', i, 'minutes before'
    checkSchVsEst.schVsEst(SAMPLE_NAME, 'GTFSScheduledTimesAA060-9', i)


