from .enum import DigitalOutput

from .. import models


class WaterLevel:

    def __init__(self, min_level, max_level):
        self.min_level = min_level
        self.max_level = max_level

    def measure_level(self):
        # TODO: what if there are no measures?
        try:
            return models.last_water_level()
        except (FileNotFoundError, ValueError):
            return 0  # TODO

    def switch_on_pump_in(self):
        if self.measure_level() >= self.max_level:
            return DigitalOutput.off

        # TODO: to be removed
        if self.measure_level() <= self.min_level:
            return DigitalOutput.on

        return DigitalOutput.any

    def switch_on_pump_out(self):
        if self.measure_level() <= self.min_level:
            return DigitalOutput.off

        return DigitalOutput.any
