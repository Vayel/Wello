from functools import partial

from .shared import Base, last_value, write_digital_output
from .pump_command import PumpCommand


class PumpInCommand(Base, PumpCommand):
    __tablename__ = 'pump_in_command'


last = partial(last_value, PumpInCommand)
write = partial(write_digital_output, PumpInCommand, 'running')
