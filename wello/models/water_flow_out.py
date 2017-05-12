from functools import partial

from .shared import Base, all, last_value, request
from .water_flow import WaterFlow
from .. import signals


class WaterFlowOut(Base, WaterFlow):
    __tablename__ = 'water_flow_out'


last = partial(last_value, WaterFlowOut)
all = partial(all, WaterFlowOut)

@request
def write(value, session=None, **kwargs):
    last_flow = last(session=session)

    if last_flow is not None and value == last_flow.flow:
        return

    session.add(WaterFlowOut(flow=value))
    signals.water_flow_out_updated.emit(value=value)

signals.update_water_flow_out.connect(write)
