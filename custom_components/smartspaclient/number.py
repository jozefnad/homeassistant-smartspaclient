"""Support for Spa Client number entities."""
# Import the device class from the component that you want to support
from . import SpaClientDevice
from .const import _LOGGER, DOMAIN, ICONS, SPA
from datetime import timedelta
from homeassistant.components.number import NumberEntity, NumberMode

SCAN_INTERVAL = timedelta(seconds=1)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Setup the Spa Client number entities."""

    spaclient = hass.data[DOMAIN][config_entry.entry_id][SPA]
    entities = []

    # Currently no number entities needed - cleanup cycle is handled by select
    # This platform is ready for future number entities if needed

    async_add_entities(entities, True)
