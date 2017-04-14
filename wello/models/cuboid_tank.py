from sqlalchemy import Integer, ForeignKey
from sqlalchemy_defaults import Column

from .shared import Base, request
from .tank import Tank


class CuboidTank(Tank):
    __tablename__ = 'cuboid_tank'
    __lazy_options__ = {}

    id = Column(Integer, ForeignKey('tank.id'), primary_key=True)
    length = Column(
        Integer,
        min=1,
        info={'label': 'Length (mm)'},
        nullable=False,
    )
    width = Column(
        Integer,
        min=1,
        info={'label': 'Width (mm)'},
        nullable=False,
    )
    height = Column(
        Integer,
        min=1,
        info={'label': 'Height (mm)'},
        nullable=False,
    )

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }

    is_cuboid = True
