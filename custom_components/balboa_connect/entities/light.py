"""Light entity for Balboa Connect."""
from __future__ import annotations

from homeassistant.components.light import LightEntity
from homeassistant.const import ENTITY_CATEGORY_CONFIG

from ..const import DOMAIN, CMD_SET_LIGHT, STATE_ON, STATE_OFF
from ..coordinator import BalboaCoordinator

class SpaLight(LightEntity):
    """Representation of a Balboa spa light."""

    def __init__(self, coordinator: BalboaCoordinator):
        """Initialize the light entity."""
        self.coordinator = coordinator
        self._attr_name = f"{coordinator.config_entry.title} Light"
        self._attr_unique_id = f"{DOMAIN}_{coordinator.config_entry.entry_id}_light"
        self._attr_is_on = False
        self._attr_brightness = 255  # Default to max brightness

    async def async_update(self) -> None:
        """Update the light state from the coordinator."""
        await self.coordinator.async_request_refresh()
        state = self.coordinator.data
        if state and "LIGHT" in state:
            self._attr_is_on = state["LIGHT"] != STATE_OFF
            if "LIGHT_LEVEL" in state:
                self._attr_brightness = int(float(state["LIGHT_LEVEL"]) * 255 / 100)

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the light on."""
        brightness = kwargs.get("brightness", 255)
        level = int(brightness / 255 * 100)
        await self.hass.async_add_executor_job(
            self.coordinator.client.send_command,
            CMD_SET_LIGHT.format(level),
        )
        self._attr_is_on = True
        self._attr_brightness = brightness
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the light off."""
        await self.hass.async_add_executor_job(
            self.coordinator.client.send_command,
            CMD_SET_LIGHT.format(0),
        )
        self._attr_is_on = False
        self.async_write_ha_state()
