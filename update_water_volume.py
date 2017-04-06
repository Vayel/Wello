import sys
import wello


if __name__ == '__main__':
    volume = int(sys.argv[1])
    print(wello.models.water_volume.write(volume))
