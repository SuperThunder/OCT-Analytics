# Automate the generation of the files wanted for analysis by running their scripts
# Note that this can take some time, especially for the schedule vs estimate stage
import toCSV
import GTFStimes
import checkSchVsEst

SAMPLE_NAME = 'sample5'

toCSV.toCSV(SAMPLE_NAME)
GTFStimes.getStopSchInfo('./google_transit_combined/stop_times.txt', 'AA060', '9')
checkSchVsEst.schVsEst('sample5', 'GTFSScheduledTimesAA060-9', 0)
checkSchVsEst.schVsEst('sample5', 'GTFSScheduledTimesAA060-9', 1)
checkSchVsEst.schVsEst('sample5', 'GTFSScheduledTimesAA060-9', 2)
