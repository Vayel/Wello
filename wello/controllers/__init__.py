from .water_volume import WaterVolume

from .. import models

io_protocol = None


def pump_in(running):
    if models.pump_in_command.write(running):
        io_protocol.command_pump_in(running)
