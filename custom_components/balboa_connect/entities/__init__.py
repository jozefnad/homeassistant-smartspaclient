"""Entities for Balboa Connect integration."""
from homeassistant.helpers.entity import Entity

from ..const import DOMAIN
from .climate import SpaClimate
from .switch import SpaSwitch
from .light import SpaLight
from .sensor import SpaTemperatureSensor
from .binary_sensor import SpaErrorBinarySensor

async def async_setup_entries(hass, config_entry, async_add_entities):
    """Set up Balboa Connect entities."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]

    # Climate entity
    async_add_entities([SpaClimate(coordinator)])

    # Switch entities (ex: Pump 1, Pump 2, Jets)
    async_add_entities([
        SpaSwitch(coordinator, "pump1", "Pompe 1", 1),
        SpaSwitch(coordinator, "pump2", "Pompe 2", 2),
        SpaSwitch(coordinator, "jets", "Jets", 3),
    ])

    # Light entity
    async_add_entities([SpaLight(coordinator)])

    # Sensor entities
    async_add_entities([SpaTemperatureSensor(coordinator)])

    # Binary sensor entities
    async_add_entities([SpaErrorBinarySensor(coordinator)])
