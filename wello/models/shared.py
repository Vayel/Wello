from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
Session = sessionmaker()


def last_value(model, session):
    return session.query(model).order_by(model.__dict__['datetime'].desc()).first()


def write_digital_output(model, field, value, session):
    last = last_value(model, session)
    if last is not None and last.__dict__[field] == value:
        return False

    session.add(model(**{field: value,}))
    return True
