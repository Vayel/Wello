from . import water_volume

from .. import exceptions, models
from . import water_volume


def pump_in(running):
    if running and water_volume.may_overflow():
        raise exceptions.TankMayOverflow()

    models.pump_in_command.write(running)
