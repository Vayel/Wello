import math

from .. import exceptions, models

TOTAL_HEIGHT = 300


def distance_to_cylindric_volume(distance, radius, height):
    total_vol = math.pi * radius**2 * height
    empty_vol = math.pi * radius**2 * distance
    return total_vol - empty_vol


def distance_to_cuboid_volume(distance, width, length, height):
    total_vol = width * length * height
    empty_vol = width * length * distance
    return total_vol - empty_vol


def distance_to_volume(distance):
    tank = models.config.tank()

    if tank.is_cylindric:
        return distance_to_cylindric_volume(distance, tank.radius, tank.height)

    if tank.is_cuboid:
        return distance_to_cuboid_volume(distance, tank.width, tank.length, tank.height)
