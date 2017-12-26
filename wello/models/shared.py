from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
Session = sessionmaker()


def request(func):
    def wrapper(*args, **kwargs):
        if kwargs.get('session', None):
            return func(*args, **kwargs)

        session = Session()
        try:
            ret = func(*args, session=session, **kwargs)
            session.commit()
            return ret
        except:
            session.rollback()
            raise
        finally:
            session.close()

    return wrapper


@request
def last_value(model, session=None):
    obj = session.query(model).order_by(model.__dict__['datetime'].desc()).first()
    if obj is not None:
        session.expunge(obj)
    return obj


@request
def all(model, session=None):
    objs = session.query(model).all()
    session.expunge_all()
    return objs


@request
def write_digital_output(model, field, running, session=None):
    last = last_value(model, session=session)
    if last is not None and last.__dict__[field] == running:
        return

    session.add(model(**{field: running,}))


class VolumeMixin:
    @property
    def litre_volume(self):
        return int(self.volume / 1000000.)
