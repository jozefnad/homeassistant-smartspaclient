"""Const file for Spa Client."""
import logging

_LOGGER = logging.getLogger(__name__)
CONF_SYNC_TIME = "sync_time"
DATA_LISTENER = "listener"
DEFAULT_SCAN_INTERVAL = 1
DOMAIN = "smartspaclient"
FILTER_CYCLE_TIMES = ["Begins", "Runs"]
MIN_SCAN_INTERVAL = 1
SPA = "spa"

SPACLIENT_COMPONENTS = [
    "binary_sensor",
    "climate",
    "light",
    "number",
    "select",
    "sensor",
    "switch",
    "time",
]

FAULT_MSG = {
    15: "Sensors are out of sync",
    16: "The water flow is low",
    17: "The water flow has failed",
    18: "The settings have been reset",
    19: "Priming Mode",
    20: "The clock has failed",
    21: "The settings have been reset",
    22: "Program memory failure",
    26: "Sensors are out of sync -- Call for service",
    27: "The heater is dry",
    28: "The heater may be dry",
    29: "The water is too hot",
    30: "The heater is too hot",
    31: "Sensor A Fault",
    32: "Sensor B Fault",
    34: "A pump may be stuck on",
    35: "Hot fault",
    36: "The GFCI test failed",
    37: "Standby Mode (Hold Mode)"
}

ICONS = {
    "Auxiliary 1": "mdi:numeric-1-circle-outline",
    "Auxiliary 2": "mdi:numeric-2-circle-outline",
    "Blower": "mdi:weather-windy",
    "Circulation Pump": "mdi:pump",
    "Cleanup Cycle": "mdi:broom",
    "Clock Mode": "mdi:clock-outline",
    "Fault Log": "mdi:archive-alert",
    "Filter Cycle": "mdi:sync",
    "GFCI Test": "mdi:shield-check",
    "Heat Mode": "mdi:alpha-r-box-outline",
    "Heating State": "mdi:fire",
    "Heater Voltage": "mdi:flash",
    "Heater Type": "mdi:water-boiler",
    "Hold Mode": "mdi:car-brake-hold",
    "M8 AI": "mdi:robot",
    "Mister": "mdi:auto-fix",
    "Model Name": "mdi:information-outline",
    "Notification": "mdi:bell",
    "Panel Lock": "mdi:lock",
    "Priming": "mdi:pump",
    "Pump 1": "mdi:pump",
    "Pump 2": "mdi:pump",
    "Pump 3": "mdi:pump",
    "Pump 4": "mdi:pump",
    "Pump 5": "mdi:pump",
    "Pump 6": "mdi:pump",
    "Reminder Type": "mdi:reminder",
    "Reminders": "mdi:bell-ring",
    "Sensor A Temperature": "mdi:thermometer",
    "Sensor B Temperature": "mdi:thermometer",
    "Settings Lock": "mdi:lock-outline",
    "Software Version": "mdi:tag",
    "Spa State": "mdi:hot-tub",
    "Spa Thermostat": "mdi:hot-tub",
    "Spa Time": "mdi:clock-digital",
    "Standby Mode": "mdi:ungroup",
    "Temperature Range": "mdi:thermometer-lines",
    "Temperature Scale": "mdi:thermometer-auto",
    "WiFi State": "mdi:wifi",
    "Flip Screen": "mdi:screen-rotation",
}
