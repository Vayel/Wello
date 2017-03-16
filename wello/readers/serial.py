from .. import models


class ManySensors:

    def __init__(self, conn):
        self.conn = conn

    def read(self):
        raise NotImplementedError()
