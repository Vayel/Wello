from functools import partial

from .shared import Base, write_digital_output
from .digital_state import DigitalState, last as last_state
from .. import signals


class UrbanNetworkState(Base, DigitalState):
    __tablename__ = 'urban_network_state'


last = partial(last_state, UrbanNetworkState)
write = partial(write_digital_output, UrbanNetworkState, 'running')
signals.urban_network_state.connect(write)
