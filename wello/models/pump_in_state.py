from functools import partial

from .shared import Base, write_digital_output
from .digital_state import DigitalState, last as last_state
from .. import signals


class PumpInState(Base, DigitalState):
    __tablename__ = 'pump_in_state'


last = partial(last_state, PumpInState)
write = partial(write_digital_output, PumpInState, 'running')
signals.pump_in_state.connect(write)
