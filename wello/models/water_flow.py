from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy_defaults import Column


class WaterFlow:
    __lazy_options__ = {}

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, auto_now=True, nullable=False)
    flow = Column(Integer, nullable=False)
