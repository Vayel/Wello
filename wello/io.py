import requests

from . import exceptions, signals, tools

TIMEOUT = 3
_card_ip = None


def init(ip):
    global _card_ip
    _card_ip = ip


def build_arduino_url(suffix):
    if _card_ip is None:
        raise exceptions.NeedInitialisation()
    return "http://" + _card_ip + "/" + suffix


def write_pump_in(running, **kwargs):
    requests.post(build_arduino_url("pump_in"), data={"state": "1" if running else "0"})


def write_urban_network(running, **kwargs):
    requests.post(build_arduino_url("urban_network"), data={"state": "1" if running else "0"})


def read_digital(url_suffix):
    return int(requests.get(build_arduino_url(url_suffix)).text)


def read_pump_in():
    state = read_digital("pump_in")
    signals.pump_in_state.emit(running=state)


def read_urban_network():
    state = read_digital("urban_network")
    print(state)
    signals.urban_network_state.emit(running=state)


def read_water_volume():
    distance = requests.get(build_arduino_url("water_distance")).text
    volume = tools.distance_to_volume(int(distance))
    signals.update_water_volume.emit(volume=volume)


def read_flowmeter_in():
    flow = requests.get(build_arduino_url("flow_in")).text
    flow = int(flow)
    signals.update_water_flow_in.emit(value=flow)


def read_flowmeter_out():
    flow = requests.get(build_arduino_url("flow_out")).text
    flow = int(flow)
    signals.update_water_flow_out.emit(value=flow)


def read_all():
    try:
        data = requests.get(build_arduino_url(""), timeout=TIMEOUT).json()
    except requests.exceptions.ConnectionError:
        signals.error.emit(msg="Impossible de contacter la carte")
        return

    signals.pump_in_state.emit(running=data["pump_in"])
    signals.urban_network_state.emit(running=data["urban_network"])
    signals.update_water_volume.emit(volume=tools.distance_to_volume(data["water_distance"]))
    signals.update_water_flow_in.emit(value=data["flow_in"])
    signals.update_water_flow_out.emit(value=data["flow_out"])
