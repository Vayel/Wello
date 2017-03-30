from sqlalchemy import DateTime, Integer
from sqlalchemy_defaults import Column

from .shared import Base, request


class Config(Base):
    __tablename__ = 'config'

    id = Column(Integer, primary_key=True)
    water_volume_max_delta = Column(  # cL
        Integer,
        min=0,
        default=0,
        info={'label': 'Water volume max delta (mm3)'},
    )
    tank_radius = Column(  # mm
        Integer,
        min=1,
        info={'label': 'Tank radius (mm)'},
    )
    tank_height = Column(  # mm
        Integer,
        min=1,
        info={'label': 'Tank height (mm)'},
    )


@request
def last(session=None):
    obj = session.query(Config).order_by(Config.id.desc()).first()
    if obj is not None:
        session.expunge(obj)
    return obj
