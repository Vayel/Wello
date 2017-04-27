from twisted.protocols.basic import LineReceiver

from .. import exceptions, signals
from . import tools


class ArduinoProtocol(LineReceiver):
    delimiter = b'\r\n'
    WATER_DISTANCE_KEY = b'WATER_DISTANCE'
    WATER_FLOW_IN_KEY = b'WATER_FLOW_IN'
    PUMP_IN_KEY = b'PUMP_IN'
    URBAN_NETWORK_KEY = b'URBAN_NETWORK'

    def parse_message(self, message):
        try:
            key, val = message.split(b'=')
        except ValueError:
            raise exceptions.BadMessageFormat()
        return key, val

    def lineReceived(self, line):
        try:
            key, val = self.parse_message(line)
        except exceptions.BadMessageFormat:
            print('Bad message format: ', line)
            return

        if key == self.WATER_DISTANCE_KEY:
            try:
                val = int(val)
                volume = tools.distance_to_volume(val)
            except (ValueError, exceptions.NeedConfiguration):
                return

            signals.update_water_volume.emit(volume=volume)
        elif key == self.PUMP_IN_KEY:
            try:
                val = bool(int(val))
            except ValueError:
                return

            signals.pump_in_state.emit(running=val)
        elif key == self.URBAN_NETWORK_KEY:
            try:
                val = bool(int(val))
            except ValueError:
                return

            signals.urban_network_state.emit(running=val)
        elif key == self.WATER_FLOW_IN_KEY:
            try:
                val = int(val)
            except ValueError:
                return

            signals.update_water_flow_in.emit(value=val)

    def write(self, key, value):
        cmd = key + b'=' + value + b';'
        self.sendLine(cmd)

    def command_pump_in(self, running, **kwargs):
        self.write(self.PUMP_IN_KEY, b'1' if running else b'0')

    def command_urban_network(self, running, **kwargs):
        self.write(self.URBAN_NETWORK_KEY, b'1' if running else b'0')
