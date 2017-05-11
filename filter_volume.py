import csv
from datetime import datetime

from scipy.signal import lfilter
import numpy as np
import matplotlib.pyplot as plt 


def read_data():
    x = []
    y = []

    with open('volumes.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            x.append(datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f'))
            y.append(int(row[1]))

    return x, y


def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')


if __name__ == '__main__':
    x, y = read_data()
    plt.plot(x, y)

    y_av = movingaverage(y, 5)
    plt.plot(x, y_av, "r")

    plt.show()
