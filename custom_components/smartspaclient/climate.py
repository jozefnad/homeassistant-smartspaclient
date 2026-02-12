"""Support for Spa Client climate device."""
# Import the device class from the component that you want to support
from . import SpaClientDevice
from .const import _LOGGER, DOMAIN, ICONS, SPA
from datetime import timedelta
from homeassistant.components.climate import ClimateEntity, ClimateEntityFeature, HVACAction, HVACMode
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.util.unit_conversion import TemperatureConverter

SCAN_INTERVAL = timedelta(seconds=1)

SUPPORT_HVAC = [HVACMode.HEAT, HVACMode.OFF]


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Setup the Spa Client climate device."""

    spaclient = hass.data[DOMAIN][config_entry.entry_id][SPA]
    entities = []

    entities.append(SpaThermostat(spaclient, config_entry))

    async_add_entities(entities, True)


class SpaThermostat(SpaClientDevice, ClimateEntity):
    """Representation of a climate device."""
    _enable_turn_on_off_backwards_compatibility = False

    def __init__(self, spaclient, config_entry):
        """Initialize the device."""
        super().__init__(spaclient, config_entry)
        self._spaclient = spaclient
        self._icon = ICONS.get('Spa Thermostat')

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return f"{self._spaclient.get_macaddr().replace(':', '')}#spa_thermostat"

    @property
    def name(self):
        """Return the name of the device."""
        return 'Spa Thermostat'

    @property
    def icon(self):
        """Return the icon of the device."""
        return self._icon

    @property
    def hvac_mode(self):
        """Return current HVAC mode based on standby mode.
        
        Standby mode ON = heating disabled (OFF)
        Standby mode OFF = heating enabled (HEAT)
        """
        if self._spaclient.get_standby_mode():
            return HVACMode.OFF
        return HVACMode.HEAT

    @property
    def hvac_action(self):
        """Return the current HVAC action.
        
        heating == 0: Off
        heating == 1: Heating
        heating == 2: Heat Waiting (preparing for heat)
        """
        if self._spaclient.get_standby_mode():
            return HVACAction.OFF
        heating = self._spaclient.get_heating()
        if heating == 1:
            return HVACAction.HEATING
        if heating == 2:
            return HVACAction.IDLE  # Heat Waiting / preparing for heat
        return HVACAction.IDLE

    @property
    def hvac_modes(self):
        """Return available HVAC modes."""
        return SUPPORT_HVAC

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.TURN_ON | ClimateEntityFeature.TURN_OFF

    @property
    def current_temperature(self):
        """Return the current temperature."""
        if self._spaclient.get_current_temp() != None:
            if self.hass.config.units.temperature_unit == UnitOfTemperature.CELSIUS and self._spaclient.temp_scale == "Fahrenheit":
                return round(TemperatureConverter.convert(self._spaclient.get_current_temp(), UnitOfTemperature.FAHRENHEIT, UnitOfTemperature.CELSIUS) * 2) / 2
            if self.hass.config.units.temperature_unit == UnitOfTemperature.CELSIUS and self._spaclient.temp_scale == "Celsius":
                return self._spaclient.get_current_temp() / 2
            if self.hass.config.units.temperature_unit == UnitOfTemperature.FAHRENHEIT and self._spaclient.temp_scale == "Celsius":
                return round(TemperatureConverter.convert(self._spaclient.get_current_temp() / 2, UnitOfTemperature.CELSIUS, UnitOfTemperature.FAHRENHEIT) * 2) / 2
            return self._spaclient.get_current_temp()
        return None

    @property
    def target_temperature(self):
        """Return the target temperature."""
        if self.hass.config.units.temperature_unit == UnitOfTemperature.CELSIUS and self._spaclient.temp_scale == "Fahrenheit":
            return round(TemperatureConverter.convert(self._spaclient.get_set_temp(), UnitOfTemperature.FAHRENHEIT, UnitOfTemperature.CELSIUS) * 2) / 2
        if self.hass.config.units.temperature_unit == UnitOfTemperature.CELSIUS and self._spaclient.temp_scale == "Celsius":
            return self._spaclient.get_set_temp() / 2
        if self.hass.config.units.temperature_unit == UnitOfTemperature.FAHRENHEIT and self._spaclient.temp_scale == "Celsius":
            return round(TemperatureConverter.convert(self._spaclient.get_set_temp() / 2, UnitOfTemperature.CELSIUS, UnitOfTemperature.FAHRENHEIT) * 2) / 2
        return self._spaclient.get_set_temp()

    async def async_set_temperature(self, **kwargs):
        temperature = kwargs[ATTR_TEMPERATURE]
        if self.hass.config.units.temperature_unit == UnitOfTemperature.CELSIUS and self._spaclient.temp_scale == "Fahrenheit":
            temperature = round(TemperatureConverter.convert(temperature, UnitOfTemperature.CELSIUS, UnitOfTemperature.FAHRENHEIT))
        if self.hass.config.units.temperature_unit == UnitOfTemperature.CELSIUS and self._spaclient.temp_scale == "Celsius":
            temperature = temperature * 2
        if self.hass.config.units.temperature_unit == UnitOfTemperature.FAHRENHEIT and self._spaclient.temp_scale == "Celsius":
            temperature = round(TemperatureConverter.convert(temperature, UnitOfTemperature.FAHRENHEIT, UnitOfTemperature.CELSIUS) * 2)
        await self._spaclient.set_temperature(temperature)

    async def async_set_hvac_mode(self, hvac_mode):
        """Set new target HVAC mode via standby mode.
        
        OFF = enable standby mode (disables heating, pumps etc still work)
        HEAT = disable standby mode (heating enabled)
        """
        if hvac_mode == HVACMode.HEAT:
            if self._spaclient.get_standby_mode():
                self._spaclient.set_standby_mode()  # Toggle off
        elif hvac_mode == HVACMode.OFF:
            if not self._spaclient.get_standby_mode():
                self._spaclient.set_standby_mode()  # Toggle on

    async def async_turn_on(self):
        """Turn on the spa (disable standby mode)."""
        if self._spaclient.get_standby_mode():
            self._spaclient.set_standby_mode()

    async def async_turn_off(self):
        """Turn off the spa (enable standby mode)."""
        if not self._spaclient.get_standby_mode():
            self._spaclient.set_standby_mode()

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        if self._spaclient.get_temp_range() == "High":
            if self.hass.config.units.temperature_unit == UnitOfTemperature.CELSIUS:
                return round(TemperatureConverter.convert(self._spaclient.get_high_range_min(), UnitOfTemperature.FAHRENHEIT, UnitOfTemperature.CELSIUS) * 2) / 2
            return TemperatureConverter.convert(self._spaclient.get_high_range_min(), UnitOfTemperature.FAHRENHEIT, self.temperature_unit)
        if self.hass.config.units.temperature_unit == UnitOfTemperature.CELSIUS:
            return round(TemperatureConverter.convert(self._spaclient.get_low_range_min(), UnitOfTemperature.FAHRENHEIT, UnitOfTemperature.CELSIUS) * 2) / 2
        return TemperatureConverter.convert(self._spaclient.get_low_range_min(), UnitOfTemperature.FAHRENHEIT, self.temperature_unit)

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        if self._spaclient.get_temp_range() == "High":
            if self.hass.config.units.temperature_unit == UnitOfTemperature.CELSIUS:
                return round(TemperatureConverter.convert(self._spaclient.get_high_range_max(), UnitOfTemperature.FAHRENHEIT, UnitOfTemperature.CELSIUS) * 2) / 2
            return TemperatureConverter.convert(self._spaclient.get_high_range_max(), UnitOfTemperature.FAHRENHEIT, self.temperature_unit)
        if self.hass.config.units.temperature_unit == UnitOfTemperature.CELSIUS:
            return round(TemperatureConverter.convert(self._spaclient.get_low_range_max(), UnitOfTemperature.FAHRENHEIT, UnitOfTemperature.CELSIUS) * 2) / 2
        return TemperatureConverter.convert(self._spaclient.get_low_range_max(), UnitOfTemperature.FAHRENHEIT, self.temperature_unit)

    @property
    def temperature_unit(self):
        """Return the unit of measurement used by the platform."""
        if self.hass.config.units.temperature_unit == UnitOfTemperature.CELSIUS:
            return UnitOfTemperature.CELSIUS
        return UnitOfTemperature.FAHRENHEIT

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attrs = {}
        attrs["Heat Mode"] = self._spaclient.get_heat_mode()
        attrs["Heating State"] = self._spaclient.get_heating_state()
        attrs["Standby Mode"] = "On" if self._spaclient.get_standby_mode() else "Off"
        attrs["Temperature Range"] = self._spaclient.get_temp_range()
        attrs["Temperature Scale"] = self._spaclient.get_temp_scale()
        return attrs

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._spaclient.get_gateway_status()
