from sqlalchemy import Integer, ForeignKey
from sqlalchemy_defaults import Column

from .shared import Base, request
from .tank import Tank


class CylinderTank(Tank):
    __tablename__ = 'cylinder_tank'
    __lazy_options__ = {}

    id = Column(Integer, ForeignKey('tank.id'), primary_key=True)
    radius = Column(
        Integer,
        min=1,
        info={'label': 'Tank radius (mm)'},
        nullable=False,
    )
    height = Column(
        Integer,
        min=1,
        info={'label': 'Tank height (mm)'},
        nullable=False,
    )

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }
