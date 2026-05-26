"""Climate entity for Balboa Connect (temperature and mode control)."""
from __future__ import annotations

from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    HVACMode,
    ClimateEntityFeature,
)
from homeassistant.const import UnitOfTemperature, ATTR_TEMPERATURE

from ..const import DOMAIN, CMD_SET_TEMP, CMD_SET_MODE
from ..coordinator import BalboaCoordinator

class SpaClimate(ClimateEntity):
    """Representation of a Balboa spa climate control."""

    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE
    )
    _attr_hvac_modes = [HVACMode.HEAT, HVACMode.OFF]
    _attr_temperature_unit = UnitOfTemperature.CELSIUS

    def __init__(self, coordinator: BalboaCoordinator):
        """Initialize the climate entity."""
        super().__init__()
        self.coordinator = coordinator
        self._attr_name = f"{coordinator.config_entry.title} Climate"
        self._attr_unique_id = f"{DOMAIN}_{coordinator.config_entry.entry_id}_climate"
        self._attr_current_temperature = None
        self._attr_target_temperature = None
        self._attr_hvac_mode = HVACMode.OFF

    async def async_update(self) -> None:
        """Update the climate state from the coordinator."""
        await self.coordinator.async_request_refresh()
        state = self.coordinator.data
        if state:
            if "TEMP" in state:
                self._attr_current_temperature = float(state["TEMP"])
            if "TARGET_TEMP" in state:
                self._attr_target_temperature = float(state["TARGET_TEMP"])
            if "MODE" in state:
                self._attr_hvac_mode = (
                    HVACMode.HEAT if state["MODE"] == "HEAT" else HVACMode.OFF
                )

    async def async_set_temperature(self, **kwargs) -> None:
        """Set new target temperature."""
        if (temp := kwargs.get(ATTR_TEMPERATURE)) is not None:
            self._attr_target_temperature = temp
            await self.hass.async_add_executor_job(
                self.coordinator.client.send_command,
                CMD_SET_TEMP.format(temp),
            )
            await self.coordinator.async_request_refresh()

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new HVAC mode."""
        self._attr_hvac_mode = hvac_mode
        mode_str = "HEAT" if hvac_mode == HVACMode.HEAT else "OFF"
        await self.hass.async_add_executor_job(
            self.coordinator.client.send_command,
            CMD_SET_MODE.format(mode_str),
        )
        await self.coordinator.async_request_refresh()
