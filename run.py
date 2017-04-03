import wello


def start(config, **kwargs):  # signalslot needs **kwargs
    thread = wello.IOThread()
    thread.configure(config)
    thread.start()

    thread = wello.ControllerThread()
    thread.configure(config)
    thread.start()


if __name__ == '__main__':
    wello.UIThread().start()

    if wello.models.config.is_valid():
        start(wello.models.config.last())
    else:
        # Do not start threads till first configuration
        wello.models.signals.configuration.connect(start)
