from time import sleep
from threading import Thread

import serial

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from . import controllers
from .controllers.enum import DigitalOutput
from . import io
from . import models
from . import ui

SERIAL_PORT = '/dev/ttyACM0'
SERIAL_BAUDRATE = 9600

engine = create_engine('sqlite:///./wello.db')
models.shared.Session.configure(bind=engine)


class UIThread(Thread):

    def run(self):
        ui.app.run()


class ControllerThread(Thread):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        models.signals.configuration.connect(self.configure)

    def configure(self, config, **kwargs):
        controllers.water_volume.init(config.min_water_volume, config.max_water_volume)

    def run(self):
        while True:
            pump_in_output = controllers.water_volume.pump_in()

            if pump_in_output == DigitalOutput.on:
                controllers.pump_in(True)
            elif pump_in_output == DigitalOutput.off:
                controllers.pump_in(False)

            sleep(0.5)  # TODO: to be determined


class IOThread(Thread):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.protocol = io.ArduinoProtocol()
        models.signals.pump_in_command.connect(self.protocol.command_pump_in)

    def configure(self, config, **kwargs):
        pass  # TODO

    def run(self):
        io.string.run(self.protocol)
        """
        io.serial.run(
            self.protocol,
            SERIAL_PORT,
            SERIAL_BAUDRATE
        )
        """
