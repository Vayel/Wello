import csv
from datetime import datetime

from scipy.signal import lfilter, butter
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


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


if __name__ == '__main__':
    x, y = read_data()
    plt.plot(x, y, label='Original')

    y_av = movingaverage(y, 5)
    plt.plot(x, y_av, "r", label='MA')

    order = 6
    fs = 30.0       # sample rate, Hz
    cutoff = 3.667  # desired cutoff frequency of the filter, Hz

    y_filter = butter_lowpass_filter(y, cutoff, fs, order)
    plt.plot(x, y_filter, "g", label='Filter')

    plt.show()
