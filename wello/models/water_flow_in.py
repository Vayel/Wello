from functools import partial

from .shared import Base, last_value, request
from .water_flow import WaterFlow
from .. import signals


class WaterFlowIn(Base, WaterFlow):
    __tablename__ = 'water_flow_in'


last = partial(last_value, WaterFlowIn)

@request
def write(value, session=None, **kwargs):
    last_flow = last(session=session)

    if last_flow is not None and value == last_flow.flow:
        return

    session.add(WaterFlowIn(flow=value))
    signals.water_flow_in_updated.emit(value=value)

signals.update_water_flow_in.connect(write)
