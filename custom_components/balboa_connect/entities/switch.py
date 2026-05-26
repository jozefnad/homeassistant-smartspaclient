"""Switch entities for Balboa Connect (pumps, jets, etc.)."""
from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.const import ENTITY_CATEGORY_CONFIG

from ..const import DOMAIN, CMD_SET_PUMP, STATE_ON, STATE_OFF
from ..coordinator import BalboaCoordinator

class SpaSwitch(SwitchEntity):
    """Representation of a Balboa spa switch (pump, jets, etc.)."""

    def __init__(
        self,
        coordinator: BalboaCoordinator,
        device_id: str,
        name: str,
        pump_id: int,
    ):
        """Initialize the switch."""
        self.coordinator = coordinator
        self.device_id = device_id
        self.pump_id = pump_id
        self._attr_name = name
        self._attr_unique_id = f"{DOMAIN}_{coordinator.config_entry.entry_id}_{device_id}"
        self._attr_is_on = False

    async def async_update(self) -> None:
        """Update the switch state from the coordinator."""
        state = await self.coordinator.async_request_refresh()
        if state and self.device_id in state:
            self._attr_is_on = state[self.device_id] == STATE_ON

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the switch on."""
        await self.hass.async_add_executor_job(
            self.coordinator.client.send_command,
            CMD_SET_PUMP.format(self.pump_id, STATE_ON),
        )
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the switch off."""
        await self.hass.async_add_executor_job(
            self.coordinator.client.send_command,
            CMD_SET_PUMP.format(self.pump_id, STATE_OFF),
        )
        self._attr_is_on = False
        self.async_write_ha_state()