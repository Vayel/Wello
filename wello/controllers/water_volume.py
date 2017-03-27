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
def pump_in():
    volume = models.water_volume.last()

    if volume is None:
        return DigitalOutput.any

    volume = volume.volume

    if volume >= _max:
        return DigitalOutput.off

    # TODO: to be removed
    if volume <= _min:
        return DigitalOutput.on

    return DigitalOutput.any


@check_init
def pump_out():
    if models.water_volume.last() <= _min:
        return DigitalOutput.off

    return DigitalOutput.any
