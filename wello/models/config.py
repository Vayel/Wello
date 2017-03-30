from sqlalchemy import DateTime, Integer, event
from sqlalchemy_defaults import Column


from . import signals
from .shared import Base, request


class Config(Base):
    __tablename__ = 'config'

    id = Column(Integer, primary_key=True)
    water_volume_max_delta = Column(  # cL
        Integer,
        min=0,
        info={'label': 'Water volume max delta (mm3)'},
        nullable=False,
    )
    tank_radius = Column(  # mm
        Integer,
        min=1,
        info={'label': 'Tank radius (mm)'},
        nullable=False,
    )
    tank_height = Column(  # mm
        Integer,
        min=1,
        info={'label': 'Tank height (mm)'},
        nullable=False,
    )


@request
def last(session=None):
    obj = session.query(Config).order_by(Config.id.desc()).first()
    if obj is not None:
        session.expunge(obj)
    return obj


def is_valid():
    return last() is not None


@event.listens_for(Config, 'after_insert')
def configuration_updated(mapper, connection, target):
    signals.configuration.emit()
