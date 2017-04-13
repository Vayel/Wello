import scipy.signal

from matplotlib import pyplot as plt

from .. import models

TOTAL_HEIGHT = 300

last_distances = [0 for i in range(20)]
last_distances_filtered = last_distances

def distance_to_volume(distance):
    # keep the last 20 distances in a list
    del last_distances[0]
    last_distances.append(TOTAL_HEIGHT - distance)
    last_distances_filtered = scipy.signal.medfilt(last_distances)

    print()
    print("Original : ", last_distances)
    print("Filtered : ", [int(i) for i in last_distances_filtered])
    
    plt.plot(last_distances)
    plt.plot(last_distances_filtered)
    plt.show()

    return TOTAL_HEIGHT - distance
