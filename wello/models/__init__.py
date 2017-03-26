from . import pump_in_command


# TODO: to be stored in database
WATER_LEVEL_FILE = 'last_water_level'


def last_water_level():
    with open(WATER_LEVEL_FILE) as f:
        return int(f.read())


def save_last_water_level(val):
    with open(WATER_LEVEL_FILE, 'w') as f:
        f.write(str(val))
