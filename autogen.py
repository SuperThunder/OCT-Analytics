# Automate the generation of the files wanted for analysis by running their scripts
# Note that this can take some time, especially for the schedule vs estimate stage
# todo: combine the latest sample database with the legacy data for a wider data range
import toCSV
import GTFStimes
import checkSchVsEst

SAMPLE_NAME = 'sample5'

toCSV.toCSV(SAMPLE_NAME)
GTFStimes.getStopSchInfo('./google_transit_combined/stop_times.txt', 'AA060', '9')
# generate the estimated time discrepancy for up to 5 minutes before a schedule stop
for i in range(0, 6):
    checkSchVsEst.schVsEst('sample5', 'GTFSScheduledTimesAA060-9', i)


