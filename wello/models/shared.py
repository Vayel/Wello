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
def write_digital_output(model, field, value, signal=None, session=None):
    last = last_value(model, session=session)
    if last is not None and last.__dict__[field] == value:
        return False

    session.add(model(**{field: value,}))

    if signal is not None:
        signal.emit(running=value)

    return True
