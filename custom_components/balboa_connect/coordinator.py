"""Coordinator for Balboa Connect."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant

from .const import SCAN_INTERVAL
from .client import BalboaClient

_LOGGER = logging.getLogger(__name__)

class BalboaCoordinator(DataUpdateCoordinator):
    """Coordinator to manage Balboa spa data updates."""

    def __init__(self, hass: HomeAssistant, client: BalboaClient) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Balboa Spa Coordinator",
            update_interval=SCAN_INTERVAL,
        )
        self.client = client

    async def async_update(self) -> dict[str, Any]:
        """Fetch the latest state from the spa."""
        try:
            state = await self.hass.async_add_executor_job(self.client.get_state)
            return state
        except Exception as e:
            _LOGGER.error("Error updating Balboa spa state: %s", e)
            return {}