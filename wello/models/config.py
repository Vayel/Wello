from sqlalchemy import DateTime, Integer, ForeignKey, event
from sqlalchemy_defaults import Column


from . import signals
from .shared import Base, request
from .tank import Tank


class Config(Base):
    __tablename__ = 'config'
    __lazy_options__ = {}

    id = Column(Integer, primary_key=True)
    water_volume_max_delta = Column(
        Integer,
        min=0,
        info={'label': 'Water volume max delta (mm3)'},
        nullable=False,
    )
    min_water_volume = Column(
        Integer,
        min=0,
        info={'label': 'Min water volume (mm3)'},
        nullable=False,
    )
    max_water_volume = Column(
        Integer,
        min=0,
        info={'label': 'Max water volume (mm3)'},
        nullable=False,
    )
    tank = Column(
        Integer,
        ForeignKey('{}.id'.format(Tank.__tablename__)),
        info={'label': 'Tank'},
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
    signals.configuration.emit(config=target)
