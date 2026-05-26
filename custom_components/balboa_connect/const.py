"""Constants for the Balboa Connect integration."""
from datetime import timedelta

VERSION = "0.1.0"
DOMAIN = "balboa_connect"
DEFAULT_NAME = "Balboa Spa"
DEFAULT_PORT = 4257
MIN_REQUEST_INTERVAL = 5  # Secondes entre chaque requête
CONNECTION_TIMEOUT = 10  # Secondes pour le timeout de connexion
SCAN_INTERVAL = timedelta(seconds=30)  # Intervalle de polling

# Configuration
CONF_HOST = "host"
CONF_PORT = "port"
CONF_NAME = "name"

# Commands
CMD_GET_STATE = "GET STATE"
CMD_SET_TEMP = "SET TEMP {}"
CMD_SET_MODE = "SET MODE {}"
CMD_SET_PUMP = "SET PUMP{} {}"
CMD_SET_LIGHT = "SET LIGHT {}"
CMD_GET_ERRORS = "GET ERRORS"

# States
STATE_ON = "ON"
STATE_OFF = "OFF"
STATE_UNAVAILABLE = "unavailable"
STATE_UNKNOWN = "unknown"

# Device classes
DEVICE_CLASS_TEMPERATURE = "temperature"
DEVICE_CLASS_POWER = "power"
