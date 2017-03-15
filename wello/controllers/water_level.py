from .abstract import Abstract
from .enum import DigitalOutput

from .. import models


class WaterLevel(Abstract):

    def __init__(self, min_level, max_level):
        self.min_level = min_level
        self.max_level = max_level

    def measure_level(self):
        # TODO: what if there are no measures?
        return models.last_water_level()

    def switch_on_pump_in(self):
        if self.measure_level() >= self.max_level:
            return DigitalOutput.off

        # TODO: when the level is low, switch the pump on

        return DigitalOutput.any

    def switch_on_pump_out(self):
        if self.measure_level() <= self.mmin_level:
            return DigitalOutput.off

        return DigitalOutput.any
