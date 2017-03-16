class OneSensor:

    def __init__(self, conn):
        self.conn = conn

    def write(self, sensor, value):
        cmd = '{}={};'.format(sensor, value)
        self.conn.write(cmd.encode('utf-8'))

    def switch_on_pump_in(self, on):
        self.write('PUMP_IN', 1 if on else 0)

    def switch_on_pump_out(self, on):
        self.write('PUMP_OUT', 1 if on else 0)
