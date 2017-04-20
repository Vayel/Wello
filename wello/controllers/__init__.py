from . import water_volume

from .. import exceptions, models, signals
from . import water_volume
from . import well_volume


def pump_in(running):
    if running and water_volume.may_overflow():
        raise exceptions.TankMayOverflow()

    state = models.pump_in_state.last()
    if state is None or state.running != running:
        signals.command_pump_in.emit(running=running)
