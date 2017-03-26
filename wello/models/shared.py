from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def last_output(model, session):
    return session.query(model).order_by(model.__dict__['datetime'].desc()).first()


def write_digital_output(model, field, value, session):
    last = last_output(model, session)
    if last is not None and last.__dict__[field] == value:
        return

    session.add(model(**{field: value,}))
