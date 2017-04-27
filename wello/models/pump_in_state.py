from functools import partial

from .shared import Base, last_value, request, write_digital_output
from .pump_state import PumpState
from .. import signals


class PumpInState(Base, PumpState):
    __tablename__ = 'pump_in_state'


@request
def last(running=None, session=None):
    if running is None:
        return last_value(PumpInState, session=session)

    obj = session.query(PumpInState).filter(PumpInState.running==running).order_by(
        PumpInState.__dict__['datetime'].desc()
    ).first()
    if obj is not None:
        session.expunge(obj)
    return obj


write = partial(write_digital_output, PumpInState, 'running')
signals.pump_in_state.connect(write)
