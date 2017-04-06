from functools import partial

from .shared import Base, last_value, write_digital_output
from .pump_state import PumpState
from .. import signals


class PumpInState(Base, PumpState):
    __tablename__ = 'pump_in_state'


last = partial(last_value, PumpInState)
write = partial(write_digital_output, PumpInState, 'running')
signals.pump_in_state.connect(write)
