"""Binary sensor entities for Balboa Connect."""
from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.const import DEVICE_CLASS_PROBLEM

from ..const import DOMAIN, STATE_ON, STATE_OFF
from ..coordinator import BalboaCoordinator

class SpaErrorBinarySensor(BinarySensorEntity):
    """Representation of a Balboa spa error binary sensor."""

    def __init__(self, coordinator: BalboaCoordinator):
        """Initialize the binary sensor."""
        self.coordinator = coordinator
        self._attr_name = f"{coordinator.config_entry.title} Error"
        self._attr_unique_id = f"{DOMAIN}_{coordinator.config_entry.entry_id}_error"
        self._attr_device_class = DEVICE_CLASS_PROBLEM
        self._attr_is_on = False

    async def async_update(self) -> None:
        """Update the binary sensor state from the coordinator."""
        state = await self.coordinator.async_request_refresh()
        if state and "ERROR" in state:
            self._attr_is_on = state["ERROR"] == STATE_ON