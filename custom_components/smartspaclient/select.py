"""Support for Spa Client select entities."""
# Import the device class from the component that you want to support
from . import SpaClientDevice
from .const import _LOGGER, DOMAIN, ICONS, SPA
from datetime import timedelta
from homeassistant.components.select import SelectEntity

SCAN_INTERVAL = timedelta(seconds=1)

CLEANUP_CYCLE_OPTIONS = [
    "Off",
    "30 min",
    "60 min",
    "90 min",
    "120 min",
    "150 min",
    "180 min",
    "210 min",
    "240 min",
]


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Setup the Spa Client select entities."""

    spaclient = hass.data[DOMAIN][config_entry.entry_id][SPA]
    entities = []

    entities.append(TemperatureScale(spaclient, config_entry))
    entities.append(ClockMode(spaclient, config_entry))
    entities.append(CleanupCycle(spaclient, config_entry))

    async_add_entities(entities, True)


class TemperatureScale(SpaClientDevice, SelectEntity):
    """Representation of the Temperature Scale select (°C / °F)."""

    def __init__(self, spaclient, config_entry):
        """Initialize the device."""
        super().__init__(spaclient, config_entry)
        self._spaclient = spaclient
        self._icon = ICONS.get('Temperature Scale')

    @property
    def unique_id(self) -> str:
        return f"{self._spaclient.get_macaddr().replace(':', '')}#temperature_scale"

    @property
    def name(self):
        return 'Temperature Scale'

    @property
    def icon(self):
        return self._icon

    @property
    def options(self):
        return ["Fahrenheit", "Celsius"]

    @property
    def current_option(self):
        return self._spaclient.get_temp_scale()

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        self._spaclient.set_temperature_scale(option)

    @property
    def available(self) -> bool:
        return self._spaclient.get_gateway_status()


class ClockMode(SpaClientDevice, SelectEntity):
    """Representation of the Clock Mode select (12 Hr / 24 Hr)."""

    def __init__(self, spaclient, config_entry):
        """Initialize the device."""
        super().__init__(spaclient, config_entry)
        self._spaclient = spaclient
        self._icon = ICONS.get('Clock Mode')

    @property
    def unique_id(self) -> str:
        return f"{self._spaclient.get_macaddr().replace(':', '')}#clock_mode"

    @property
    def name(self):
        return 'Clock Mode'

    @property
    def icon(self):
        return self._icon

    @property
    def options(self):
        return ["12 Hr", "24 Hr"]

    @property
    def current_option(self):
        return self._spaclient.get_time_scale()

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        self._spaclient.set_clock_mode(option)

    @property
    def available(self) -> bool:
        return self._spaclient.get_gateway_status()


class CleanupCycle(SpaClientDevice, SelectEntity):
    """Representation of the Cleanup Cycle select."""

    def __init__(self, spaclient, config_entry):
        """Initialize the device."""
        super().__init__(spaclient, config_entry)
        self._spaclient = spaclient
        self._icon = ICONS.get('Cleanup Cycle')

    @property
    def unique_id(self) -> str:
        return f"{self._spaclient.get_macaddr().replace(':', '')}#cleanup_cycle"

    @property
    def name(self):
        return 'Cleanup Cycle'

    @property
    def icon(self):
        return self._icon

    @property
    def options(self):
        return CLEANUP_CYCLE_OPTIONS

    @property
    def current_option(self):
        value = self._spaclient.get_pref_clean_up_cycle()
        if value == 0:
            return "Off"
        return f"{value * 30} min"

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        if option == "Off":
            self._spaclient.set_cleanup_cycle(0)
        else:
            # Parse "30 min" -> 1, "60 min" -> 2, etc.
            minutes = int(option.replace(" min", ""))
            self._spaclient.set_cleanup_cycle(minutes // 30)

    @property
    def available(self) -> bool:
        return self._spaclient.get_gateway_status()
