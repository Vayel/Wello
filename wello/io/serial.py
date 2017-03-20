from twisted.internet import reactor
from twisted.internet.serialport import SerialPort


def run(protocol, port, baudrate):
    SerialPort(
        protocol,
        port,
        reactor,
        baudrate=baudrate
    )
    reactor.run(installSignalHandlers=False)
