import csv
from datetime import datetime

from scipy.signal import lfilter
import matplotlib.pyplot as plt 


x = []
y = []

with open('volumes.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        x.append(datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f'))
        y.append(int(row[1]))

plt.plot(x, y)
plt.show()
