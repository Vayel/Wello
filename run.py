import wello


def start(**kwargs):  # signalslot needs **kwargs
    wello.IOThread().start()
    wello.ControllerThread().start()


if __name__ == '__main__':
    wello.UIThread().start()

    if wello.models.config.is_valid():
        start()
    else:
        wello.models.signals.configuration.connect(start)
