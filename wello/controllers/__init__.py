from .water_volume import WaterVolume

from .. import models

io_protocol = None


def pump_in(running):
    with models.open_session() as session:
        write = models.pump_in_command.write(running, session)
    if write:
        io_protocol.command_pump_in(running)
