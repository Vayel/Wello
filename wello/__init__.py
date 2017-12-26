from time import sleep
from threading import Thread

import serial

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from . import controllers
from .controllers.enum import DigitalOutput
from . import io
from . import models
from . import signals
from . import ui

SERIAL_PORT = '/dev/ttyACM0'
SERIAL_BAUDRATE = 9600

engine = create_engine('sqlite:///./wello.db')
models.shared.Session.configure(bind=engine)


class UIThread(Thread):

    def run(self):
        ui.socketio.run(ui.app)


class ControllerThread(Thread):

    @staticmethod
    def configure(config, **kwargs):
        io.init(config.card_ip)
        controllers.water_volume.init(config.min_water_volume, config.max_water_volume)
        controllers.well_volume.init(config.well_filling_delay, config.min_flow_in)

    def run(self):
        while True:
            sleep(1)  # TODO: to be determined

            io.read_all()

            # Pump in
            water_volume_output = controllers.water_volume.pump_in()
            well_volume_output = controllers.well_volume.pump_in()

            if water_volume_output == DigitalOutput.off or well_volume_output == DigitalOutput.off:
                controllers.pump_in(False)

            elif well_volume_output == DigitalOutput.on:
                controllers.pump_in(True)

            # Urban network
            water_volume_output = controllers.water_volume.urban_network()

            if water_volume_output == DigitalOutput.on:
                controllers.urban_network(True)
            elif water_volume_output == DigitalOutput.off:
                controllers.urban_network(False)


signals.configuration.connect(ControllerThread.configure)
signals.command_pump_in.connect(io.write_pump_in)
signals.command_urban_network.connect(io.write_urban_network)
