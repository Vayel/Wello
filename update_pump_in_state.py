import sys
import wello


if __name__ == '__main__':
    running = bool(int(sys.argv[1]))
    print(wello.models.pump_in_state.write(running))
