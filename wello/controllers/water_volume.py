from .enum import DigitalOutput

from .. import exceptions, models

_min = None
_max = None


def init(min_, max_):
    global _min, _max

    min_, max_ = int(min_), int(max_)

    if min_ >= max_:
        raise ValueError()

    _min, _max = min_, max_


def check_init(func):
    def wrapper(*args, **kwargs):
        if _min is None or _max is None:
            raise exceptions.NeedInitialisation()

        return func(*args, **kwargs)
    return wrapper


@check_init
def may_overflow():
    volume = models.water_volume.last()
    return volume is None or volume.volume >= _max


@check_init
def pump_in():
    volume = models.water_volume.last()

    if volume is None:
        return DigitalOutput.off

    volume = volume.volume

    if volume >= _max:
        return DigitalOutput.off

    if volume <= _min:
        return DigitalOutput.on

    return DigitalOutput.any


@check_init
def urban_network():
    volume = models.water_volume.last()

    if volume is None or volume.volume <= _min:
        return DigitalOutput.on

    return DigitalOutput.off
