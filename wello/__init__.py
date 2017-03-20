from time import sleep
from threading import Thread

import serial

from . import controllers
from .controllers.enum import DigitalOutput
from . import io
from . import ui

SERIAL_PORT = '/dev/ttyACM0'
SERIAL_BAUDRATE = 9600

io_protocol = io.ArduinoProtocol()


class UIThread(Thread):

    def run(self):
        ui.app.run()


class ControllerThread(Thread):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.water_level = controllers.WaterLevel(50, 200)

    def run(self):
        while True:
            if self.water_level.switch_on_pump_in() == DigitalOutput.on:
                io_protocol.switch_on_pump_in(True)
            elif self.water_level.switch_on_pump_in() == DigitalOutput.off:
                io_protocol.switch_on_pump_in(False)

            if self.water_level.switch_on_pump_out() == DigitalOutput.on:
                io_protocol.switch_on_pump_out(True)
            elif self.water_level.switch_on_pump_out() == DigitalOutput.off:
                io_protocol.switch_on_pump_out(False)

            sleep(0.05)


class IOThread(Thread):

    def run(self):
        io.serial.run(
            io_protocol,
            SERIAL_PORT,
            SERIAL_BAUDRATE
        )
