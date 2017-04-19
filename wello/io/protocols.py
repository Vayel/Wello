from twisted.protocols.basic import LineReceiver

from .. import exceptions, signals
from . import tools


class ArduinoProtocol(LineReceiver):
    delimiter = b'\r\n'
    WATER_DISTANCE_KEY = b'WATER_DISTANCE'
    WATER_FLOW_IN_KEY = b'WATER_FLOW_IN'
    PUMP_IN_KEY = b'PUMP_IN'
    PUMP_OUT_KEY = b'PUMP_OUT'

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
            except (ValueError, exceptions.NeedConfiguration) as e:
                return

            signals.update_water_volume.emit(volume=volume)
        elif key == self.PUMP_IN_KEY:
            try:
                val = bool(int(val))
            except ValueError as e:
                return

            signals.pump_in_state.emit(running=val)
        elif key == self.WATER_FLOW_IN_KEY:
            try:
                val = int(val)
            except ValueError as e:
                return

            signals.update_water_flow_in.emit(value=val)

    def write(self, key, value):
        cmd = key + b'=' + value + b';'
        self.sendLine(cmd)

    def command_pump_in(self, running, **kwargs):
        self.write(self.PUMP_IN_KEY, b'1' if running else b'0')

    def command_pump_out(self, running, **kwargs):
        self.write(self.PUMP_OUT_KEY, b'1' if running else b'0')
