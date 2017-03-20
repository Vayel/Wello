from twisted.protocols.basic import LineReceiver

from .. import models


class ArduinoProtocol(LineReceiver):
    delimiter = b'\r\n'

    def connectionMade(self):
        print('Connected')

    def lineReceived(self, line):
        print(line)
        try:
            val = int(line)
        except ValueError:
            return

        models.save_last_water_level(val)

    def write_sensor(self, sensor, value):
        cmd = '{}={};'.format(sensor, value)
        self.sendLine(cmd.encode('utf-8'))

    def switch_on_pump_in(self, on):
        self.write_sensor('PUMP_IN', 1 if on else 0)

    def switch_on_pump_out(self, on):
        self.write_sensor('PUMP_OUT', 1 if on else 0)
