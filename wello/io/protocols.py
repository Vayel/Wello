from twisted.protocols.basic import LineReceiver

from .. import exceptions, models
from . import tools


class ArduinoProtocol(LineReceiver):
    delimiter = b'\r\n'
    WATER_DISTANCE_KEY = b'WATER_DISTANCE'

    def parse_message(self, message):
        try:
            sensor, val = message.split(b'=')
        except ValueError:
            raise exceptions.BadMessageFormat()
        return sensor, val

    def lineReceived(self, line):
        try:
            sensor, val = self.parse_message(line)
        except exceptions.BadMessageFormat:
            print('bad message format: ', line)
            return

        if sensor == self.WATER_DISTANCE_KEY:
            try:
                val = int(val)
                volume = tools.distance_to_volume(val)
            except ValueError as e:
                print(e)
                return

            print('Volume: ', volume)
            models.water_volume.write(volume)
        else:
            print('unknown sensor ', sensor)

    def write_sensor(self, sensor, value):
        cmd = '{}={};'.format(sensor, value)
        self.sendLine(cmd.encode('utf-8'))

    def command_pump_in(self, running):
        self.write_sensor('PUMP_IN', 1 if running else 0)

    def command_pump_out(self, running):
        self.write_sensor('PUMP_OUT', 1 if running else 0)
