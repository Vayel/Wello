from sqlalchemy import DateTime, Integer, ForeignKey, event
from sqlalchemy.orm import relationship, with_polymorphic
from sqlalchemy_defaults import Column


from .. import exceptions, signals
from .shared import Base, request
from .tank import Tank
from .cuboid_tank import CuboidTank
from .cylinder_tank import CylinderTank


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
    well_filling_delay = Column(
        Integer,
        min=0,
        info={'label': 'Well filling delay (s)'},
        nullable=False,
    )
    min_flow_in = Column(
        Integer,
        min=0,
        info={'label': 'Min flow in (mm3/s)'},
        nullable=False,
    )
    tank = relationship(Tank, lazy='subquery')
    tank_id = Column(
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


@request
def tank(session=None):
    cfg = last()

    if cfg is None:
        raise exceptions.NeedConfiguration()

    entity = with_polymorphic(Tank, [CuboidTank, CylinderTank])
    obj = session.query(entity).filter(Tank.id == cfg.tank_id).one()

    if obj is not None:
        session.expunge(obj)

    return obj


def is_valid():
    return last() is not None


@event.listens_for(Config, 'after_insert')
def configuration_updated(mapper, connection, target):
    signals.configuration.emit(config=target)
