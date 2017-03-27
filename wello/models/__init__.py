from contextlib import contextmanager

import sqlalchemy
from sqlalchemy_defaults import make_lazy_configured

from . import config
from .config import Config
from .shared import Session
from . import pump_in_command
from . import water_volume

make_lazy_configured(sqlalchemy.orm.mapper)


@contextmanager
def open_session():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def add(session, *args):
    for obj in args:
        session.add(obj)
