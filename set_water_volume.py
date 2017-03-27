import sys
import wello


if __name__ == '__main__':
    volume = int(sys.argv[1])
    with wello.models.open_session() as session:
        print(wello.models.water_volume.write(volume, session))
