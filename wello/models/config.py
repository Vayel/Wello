from sqlalchemy import DateTime, Integer
from sqlalchemy_defaults import Column

from .shared import Base, request


class Config(Base):
    __tablename__ = 'config'

    id = Column(Integer, primary_key=True)
    water_volume_max_delta = Column(Integer, min=0, default=0)  # cL


@request
def last(session=None):
    obj = session.query(Config).order_by(Config.id.desc()).first()
    session.expunge(obj)
    return obj
