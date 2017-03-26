from time import sleep
from threading import Thread

import serial

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from . import controllers
from .controllers.enum import DigitalOutput
from . import io
from . import ui

SERIAL_PORT = '/dev/ttyACM0'
SERIAL_BAUDRATE = 9600

io_protocol = io.ArduinoProtocol()

engine = create_engine('sqlite:///./wello.db')

controllers.io_protocol = io_protocol
controllers.DBSession = sessionmaker(bind=engine)


class UIThread(Thread):

    def run(self):
        ui.app.run()


class ControllerThread(Thread):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.water_level = controllers.WaterLevel(50, 200)

    def run(self):
        while True:
            if self.water_level.pump_in() == DigitalOutput.on:
                controllers.pump_in(True)
            elif self.water_level.pump_in() == DigitalOutput.off:
                controllers.pump_in(False)

            sleep(2)


class IOThread(Thread):

    def run(self):
        io.string.run(io_protocol)
        """
        io.serial.run(
            io_protocol,
            SERIAL_PORT,
            SERIAL_BAUDRATE
        )
        """
