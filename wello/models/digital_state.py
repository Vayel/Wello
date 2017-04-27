from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy_defaults import Column

from .shared import last_value, request


class DigitalState:
    __lazy_options__ = {}

    id = Column(Integer, primary_key=True)
    running = Column(Boolean, nullable=False)
    datetime = Column(DateTime, auto_now=True, nullable=False)


@request
def last(model, running=None, session=None):
    if running is None:
        return last_value(model, session=session)

    obj = session.query(model).filter(model.running == running).order_by(
        model.__dict__['datetime'].desc()
    ).first()
    if obj is not None:
        session.expunge(obj)
    return obj
