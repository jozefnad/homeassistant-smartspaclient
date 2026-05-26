"""Sensor entities for Balboa Connect."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfTemperature, DEVICE_CLASS_TEMPERATURE

from ..const import DOMAIN, DEVICE_CLASS_TEMPERATURE
from ..coordinator import BalboaCoordinator

class SpaTemperatureSensor(SensorEntity):
    """Representation of a Balboa spa temperature sensor."""

    def __init__(self, coordinator: BalboaCoordinator):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._attr_name = f"{coordinator.config_entry.title} Temperature"
        self._attr_unique_id = f"{DOMAIN}_{coordinator.config_entry.entry_id}_temp"
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_device_class = DEVICE_CLASS_TEMPERATURE
        self._attr_native_value = None

    async def async_update(self) -> None:
        """Update the sensor state from the coordinator."""
        state = await self.coordinator.async_request_refresh()
        if state and "TEMP" in state:
            self._attr_native_value = float(state["TEMP"])