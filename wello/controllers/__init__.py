from .water_level import WaterLevel

from .. import models

io_protocol = None
DBSession = None


def model_writer(func):
    def wrapper(*args, **kwargs):
        session = DBSession()

        ret = func(*args, session, **kwargs)

        session.commit()
        session.close()

        return ret

    return wrapper


@model_writer
def pump_in(running, session):
    io_protocol.command_pump_in(running)
    models.pump_in_command.write(running, session)
