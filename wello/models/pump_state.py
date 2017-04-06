from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy_defaults import Column


class PumpState:
    __lazy_options__ = {}

    id = Column(Integer, primary_key=True)
    running = Column(Boolean, nullable=False)
    datetime = Column(DateTime, auto_now=True, nullable=False)
