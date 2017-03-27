from . import water_volume

from .. import exceptions, models
from . import water_volume

io_protocol = None


def check_init(func):
    def wrapper(*args, **kwargs):
        if io_protocol is None:
            raise exceptions.NeedInitialisation()

        return func(*args, **kwargs)
    return wrapper


@check_init
def pump_in(running):
    if running and water_volume.may_overflow():
        raise exceptions.TankMayOverflow()

    if models.pump_in_command.write(running):
        io_protocol.command_pump_in(running)
