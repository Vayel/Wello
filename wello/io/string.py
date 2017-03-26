import os
import sys

from twisted.internet.stdio import StandardIO
from twisted.internet import reactor


def run(protocol):
    StandardIO(protocol)
    reactor.run(installSignalHandlers=False)
