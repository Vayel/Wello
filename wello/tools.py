import math

from . import exceptions, models


def distance_to_cylindric_volume(distance, radius, height):
    vol = math.pi * radius**2 * (height - distance)
    return max(0, vol)


def distance_to_cuboid_volume(distance, width, length, height):
    vol = width * length * (height - distance)
    return max(0, vol)


def distance_to_volume(distance):
    tank = models.config.tank()

    if tank.is_cylindric:
        return distance_to_cylindric_volume(distance, tank.radius, tank.height)

    if tank.is_cuboid:
        return distance_to_cuboid_volume(distance, tank.width, tank.length, tank.height)
