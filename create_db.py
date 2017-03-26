from wello import engine
from wello.models.shared import Base


if __name__ == '__main__':
    Base.metadata.create_all(engine)
