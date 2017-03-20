import wello


if __name__ == '__main__':
    wello.UIThread().start()
    wello.IOThread().start()
    wello.ControllerThread().start()
