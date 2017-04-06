from functools import partial

from sqlalchemy import DateTime, Integer
from sqlalchemy_defaults import Column

from .shared import Base, last_value, request
from . import config
from .. import exceptions, signals


class WaterVolume(Base):
    __lazy_options__ = {}
    __tablename__ = 'water_volume'

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, auto_now=True, nullable=False)
    volume = Column(Integer, nullable=False)  # cL


last = partial(last_value, WaterVolume)

@request
def write(volume, session=None, **kwargs):
    cfg = config.last(session=session)
    last_volume = last(session=session)

    if cfg is None:
        raise exceptions.NeedConfiguration()

    if last_volume is not None and abs(last_volume.volume - volume) < cfg.water_volume_max_delta:
        return False

    session.add(WaterVolume(volume=volume))
    signals.water_volume_updated.emit(volume=volume)

    return True

signals.update_water_volume.connect(write)
