from functools import partial

from sqlalchemy import DateTime, Integer
from sqlalchemy_defaults import Column

from .shared import Base, last_value, request
from . import exceptions, config


class WaterVolume(Base):
    __lazy_options__ = {}
    __tablename__ = 'water_volume'

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, auto_now=True, nullable=False)
    volume = Column(Integer, nullable=False)  # cL


last = partial(last_value, WaterVolume)

@request
def write(value, session=None):
    cfg = config.last(session=session)
    last_volume = last(session=session)

    if cfg is None:
        raise exceptions.NeedConfiguration()

    if last_volume is not None and abs(last_volume.volume - value) < cfg.water_volume_max_delta:
        return False

    session.add(WaterVolume(volume=value))

    return True
