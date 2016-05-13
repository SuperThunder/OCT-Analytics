# Used the files generated by autogen and automatically run the needed analysis modules
# Keep them separate to avoid large overhead of regenerating data files
import sklearn_test3
import pandastest2

for i in range(0, 6):
    sklearn_test3.genpredictions('currentsample Attributes and Time Discrepencies t-%dmins'%i)

pandastest2.plotpoints('currentsampleCSV', 'Index', 'TimeToNext', 'Index vs TimeToNext Values', 'TimeToNext')
''' # This shows the sort of random spread of discrepancies (although concentrated around 0)
pandastest2.plotpoints('currentsample Attributes and Time Discrepencies t-4mins', 'Index', 'Discrepancy',
                       'Discrepancy vs Index', 'Discrepancy')
'''
SVR_FILE_NAMES = []
SVR_FILE_LABELS = []
for i in range(0, 6):
    name = './Machine learning results/SVR Predictions for currentsample Attributes and Time Discrepencies t-%dmins'%i
    label = 't-%d'%i
    SVR_FILE_NAMES.append(name)
    SVR_FILE_LABELS.append(label)

SVC_FILE_NAMES = []
SVC_FILE_LABELS = []
for i in range(0, 6):
    name = './Machine learning results/SVC Predictions for currentsample Attributes and Time Discrepencies t-%dmins'%i
    label = 't-%d'%i
    SVC_FILE_NAMES.append(name)
    SVC_FILE_LABELS.append(label)


pandastest2.multiplotlinesdt(SVR_FILE_NAMES, SVR_FILE_LABELS, 'Index', 'SVR Predicted Discrepancy',
                               'SVR Predicted Discrepancy vs Weekdays at Scheduled Arrival Time',
                               'Predicted Discrepancy')
pandastest2.multiplotlinesdt(SVC_FILE_NAMES, SVC_FILE_LABELS, 'Index', 'SVC Predicted Discrepancy',
                           'SVC Predicted Discrepancy vs Weekdays at Scheduled Arrival Time', 'Predicted Discrepancy')


'''
pandastest2.multiplotlines(SVR_FILE_NAMES, SVR_FILE_LABELS, 'Index', 'SVR Predicted Discrepancy',
                           'SVR Predicted Discrepancy vs Weekdays at Scheduled Arrival Time', 'Predicted Discrepancy')
pandastest2.multiplotlines(SVC_FILE_NAMES, SVC_FILE_LABELS, 'Index', 'SVC Predicted Discrepancy',
                      'SVC Predicted Discrepancy vs Weekdays at Scheduled Arrival Time', 'Predicted Discrepancy')
'''