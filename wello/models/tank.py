from sqlalchemy import Integer, String
from sqlalchemy_defaults import Column

from .shared import Base, request


class Tank(Base):
    __tablename__ = 'tank'

    id = Column(Integer, primary_key=True)
    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
        'polymorphic_on': type
    }

    is_cuboid = False
    is_cylindric = False

    @property
    def volume(self):
        raise NotImplementedError()


@request
def get(id_, session=None):
    obj = session.query(Tank).get(id_)
    if obj is not None:
        session.expunge(obj)
    return obj
