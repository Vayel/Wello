from time import sleep
from threading import Thread

import serial

from . import controllers
from .controllers import DigitalOutput
from . import elec
from . import models
from . import readers
from . import ui
from . import writers

ser = serial.Serial('')


class UIThread(Thread):

    def run(self):
        ui.app.run()


class ControllerThread(Thread):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.water_level = controllers.WaterLevel(5, 100)
        self.writer = writers.serial.OneSensor(ser)

    def run(self):
        while True:
            if self.water_level.switch_on_pump_in() == DigitalOutput.on:
                self.writer.switch_on_pump_in(True)
            elif self.water_level.switch_on_pump_in() == DigitalOutput.off:
                self.writer.switch_on_pump_in(False)

            if self.water_level.switch_on_pump_out() == DigitalOutput.on:
                self.writer.switch_on_pump_out(True)
            elif self.water_level.switch_on_pump_out() == DigitalOutput.off:
                self.writer.switch_on_pump_out(False)

            sleep(1)


class ReaderThread(Thread):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reader = readers.serial.ManySensors(ser)

    def run(self):
        while True:
            self.reader.read()
