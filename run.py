import wello


if __name__ == '__main__':
    wello.UIThread().start()
    wello.ControllerThread().start()
    wello.ReaderThread().start()
