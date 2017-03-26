import datetime

from sqlalchemy import Column, Boolean, DateTime, Integer


class PumpCommand:
    id = Column(Integer, primary_key=True)
    running = Column(Boolean)
    datetime = Column(DateTime, default=datetime.datetime.utcnow)
