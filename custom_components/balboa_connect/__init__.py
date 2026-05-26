
"""The Balboa Connect integration for Home Assistant."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import BalboaCoordinator
from .client import BalboaClient

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [
    Platform.CLIMATE,
    Platform.SWITCH,
    Platform.LIGHT,
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Balboa Connect from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Initialize client and coordinator
    client = BalboaClient(
        host=entry.data["host"],
        port=entry.data.get("port", 4257),
    )
    coordinator = BalboaCoordinator(hass, client=client)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "coordinator": coordinator,
    }

    # Setup platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        # Close the client connection
        client = hass.data[DOMAIN][entry.entry_id]["client"]
        client.close()
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
