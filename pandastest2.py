import matplotlib.pyplot as plt
import pandas as pd

FILE_NAME = 'sample5CSV.csv'
with open(FILE_NAME, 'rb') as sample:
    data = pd.read_csv(sample, parse_dates=True, na_values=['-50','-100'])
    indexes =  list(range(len(data)))
    plt.plot(indexes, data['TimeToNext'], linestyle='None', marker='o', color='g')
    plt.xlabel('Index')
    plt.ylabel('TimeToNext')
    plt.title('Index vs TimeToNext')
    plt.show()