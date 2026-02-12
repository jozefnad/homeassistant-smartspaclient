"""Support for Spa Client sensors."""
# Import the device class from the component that you want to support
from . import SpaClientDevice
from .const import _LOGGER, DOMAIN, ICONS, FAULT_MSG, SPA
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import EntityCategory

SCAN_INTERVAL = timedelta(seconds=1)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Spa Client sensors."""

    spaclient = hass.data[DOMAIN][config_entry.entry_id][SPA]
    entities = []

    entities.append(SpaFaultLog(spaclient, config_entry))
    entities.append(SpaHeatingState(spaclient, config_entry))
    entities.append(SpaSpaState(spaclient, config_entry))
    entities.append(SpaTime(spaclient, config_entry))
    entities.append(SpaWiFiState(spaclient, config_entry))
    entities.append(SpaReminderType(spaclient, config_entry))
    entities.append(SpaSensorATemp(spaclient, config_entry))
    entities.append(SpaSensorBTemp(spaclient, config_entry))
    entities.append(SpaGFCITest(spaclient, config_entry))
    entities.append(SpaModelName(spaclient, config_entry))
    entities.append(SpaSoftwareVersion(spaclient, config_entry))
    entities.append(SpaHeaterVoltage(spaclient, config_entry))
    entities.append(SpaHeaterType(spaclient, config_entry))
    entities.append(SpaConfigSignature(spaclient, config_entry))

    async_add_entities(entities, True)


class SpaFaultLog(SpaClientDevice, SensorEntity):
    """Representation of the fault log sensor."""

    def __init__(self, spaclient, config_entry):
        """Initialize the device."""
        super().__init__(spaclient, config_entry)
        self._spaclient = spaclient
        self._icon = ICONS.get('Fault Log')

    @property
    def unique_id(self) -> str:
        return f"{self._spaclient.get_macaddr().replace(':', '')}#fault_log"

    @property
    def name(self):
        return 'Last Known Fault'

    @property
    def icon(self):
        return self._icon

    @property
    def native_value(self):
        return FAULT_MSG.get(self._spaclient.get_fault_log_msg_code())

    @property
    def extra_state_attributes(self):
        attrs = {}
        attrs["Fault Code"] = self._spaclient.fault_log_msg_code
        attrs["Days Ago"] = self._spaclient.fault_log_days_ago
        attrs["Time"] = f"{self._spaclient.fault_log_msg_hour:02d}:{self._spaclient.fault_log_msg_minute:02d}"
        attrs["Total Entries"] = self._spaclient.fault_log_total_entries
        attrs["Set Temp"] = self._spaclient.fault_log_set_temp
        attrs["Sensor A Temp"] = self._spaclient.fault_log_sensor_a_temp
        attrs["Sensor B Temp"] = self._spaclient.fault_log_sensor_b_temp
        return attrs

    @property
    def available(self) -> bool:
        return self._spaclient.get_gateway_status()


class SpaHeatingState(SpaClientDevice, SensorEntity):
    """Representation of the heating state sensor (Off/Heating/Heat Waiting)."""

    def __init__(self, spaclient, config_entry):
        super().__init__(spaclient, config_entry)
        self._spaclient = spaclient
        self._icon = ICONS.get('Heating State')

    @property
    def unique_id(self) -> str:
        return f"{self._spaclient.get_macaddr().replace(':', '')}#heating_state"

    @property
    def name(self):
        return 'Heating State'

    @property
    def icon(self):
        if self._spaclient.get_heating_state() == "Heating":
            return "mdi:fire"
        elif self._spaclient.get_heating_state() == "Heat Waiting":
            return "mdi:fire-alert"
        return "mdi:fire-off"

    @property
    def native_value(self):
        return self._spaclient.get_heating_state()

    @property
    def extra_state_attributes(self):
        attrs = {}
        attrs["Heat Mode"] = self._spaclient.get_heat_mode()
        attrs["Temperature Range"] = self._spaclient.get_temp_range()
        return attrs

    @property
    def available(self) -> bool:
        return self._spaclient.get_gateway_status()


class SpaSpaState(SpaClientDevice, SensorEntity):
    """Representation of the spa state sensor (Running/Initializing/Hold Mode/Test Mode)."""

    def __init__(self, spaclient, config_entry):
        super().__init__(spaclient, config_entry)
        self._spaclient = spaclient
        self._icon = ICONS.get('Spa State')

    @property
    def unique_id(self) -> str:
        return f"{self._spaclient.get_macaddr().replace(':', '')}#spa_state"

    @property
    def name(self):
        return 'Spa State'

    @property
    def icon(self):
        return self._icon

    @property
    def native_value(self):
        return self._spaclient.get_spa_state()

    @property
    def available(self) -> bool:
        return self._spaclient.get_gateway_status()


class SpaTime(SpaClientDevice, SensorEntity):
    """Representation of the spa clock sensor."""

    def __init__(self, spaclient, config_entry):
        super().__init__(spaclient, config_entry)
        self._spaclient = spaclient
        self._icon = ICONS.get('Spa Time')

    @property
    def unique_id(self) -> str:
        return f"{self._spaclient.get_macaddr().replace(':', '')}#spa_time"

    @property
    def name(self):
        return 'Spa Time'

    @property
    def icon(self):
        return self._icon

    @property
    def native_value(self):
        return self._spaclient.get_current_time()

    @property
    def extra_state_attributes(self):
        attrs = {}
        attrs["Clock Mode"] = self._spaclient.get_time_scale()
        return attrs

    @property
    def available(self) -> bool:
        return self._spaclient.get_gateway_status()


class SpaWiFiState(SpaClientDevice, SensorEntity):
    """Representation of the WiFi state sensor."""

    def __init__(self, spaclient, config_entry):
        super().__init__(spaclient, config_entry)
        self._spaclient = spaclient
        self._icon = ICONS.get('WiFi State')

    @property
    def unique_id(self) -> str:
        return f"{self._spaclient.get_macaddr().replace(':', '')}#wifi_state"

    @property
    def name(self):
        return 'WiFi State'

    @property
    def icon(self):
        if self._spaclient.get_wifi_state() == 0:
            return "mdi:wifi"
        return "mdi:wifi-alert"

    @property
    def native_value(self):
        return self._spaclient.get_wifi_state_text()

    @property
    def entity_category(self):
        return EntityCategory.DIAGNOSTIC

    @property
    def available(self) -> bool:
        return self._spaclient.get_gateway_status()


class SpaReminderType(SpaClientDevice, SensorEntity):
    """Representation of the reminder type sensor."""

    def __init__(self, spaclient, config_entry):
        super().__init__(spaclient, config_entry)
        self._spaclient = spaclient
        self._icon = ICONS.get('Reminder Type')

    @property
    def unique_id(self) -> str:
        return f"{self._spaclient.get_macaddr().replace(':', '')}#reminder_type"

    @property
    def name(self):
        return 'Reminder'

    @property
    def icon(self):
        return self._icon

    @property
    def native_value(self):
        return self._spaclient.get_reminder_type_text()

    @property
    def available(self) -> bool:
        return self._spaclient.get_gateway_status()


class SpaSensorATemp(SpaClientDevice, SensorEntity):
    """Representation of the Sensor A temperature."""

    def __init__(self, spaclient, config_entry):
        super().__init__(spaclient, config_entry)
        self._spaclient = spaclient
        self._icon = ICONS.get('Sensor A Temperature')

    @property
    def unique_id(self) -> str:
        return f"{self._spaclient.get_macaddr().replace(':', '')}#sensor_a_temp"

    @property
    def name(self):
        return 'Sensor A Temperature'

    @property
    def icon(self):
        return self._icon

    @property
    def device_class(self):
        return SensorDeviceClass.TEMPERATURE

    @property
    def native_unit_of_measurement(self):
        if self._spaclient.get_temp_scale() == "Celsius":
            return "°C"
        return "°F"

    @property
    def native_value(self):
        temp = self._spaclient.get_sensor_a_temp()
        if temp is None:
            return None
        if self._spaclient.get_temp_scale() == "Celsius":
            return temp / 2
        return temp

    @property
    def available(self) -> bool:
        return self._spaclient.get_gateway_status()


class SpaSensorBTemp(SpaClientDevice, SensorEntity):
    """Representation of the Sensor B temperature."""

    def __init__(self, spaclient, config_entry):
        super().__init__(spaclient, config_entry)
        self._spaclient = spaclient
        self._icon = ICONS.get('Sensor B Temperature')

    @property
    def unique_id(self) -> str:
        return f"{self._spaclient.get_macaddr().replace(':', '')}#sensor_b_temp"

    @property
    def name(self):
        return 'Sensor B Temperature'

    @property
    def icon(self):
        return self._icon

    @property
    def device_class(self):
        return SensorDeviceClass.TEMPERATURE

    @property
    def native_unit_of_measurement(self):
        if self._spaclient.get_temp_scale() == "Celsius":
            return "°C"
        return "°F"

    @property
    def native_value(self):
        temp = self._spaclient.get_sensor_b_temp()
        if temp is None:
            return None
        if self._spaclient.get_temp_scale() == "Celsius":
            return temp / 2
        return temp

    @property
    def available(self) -> bool:
        return self._spaclient.get_gateway_status()


class SpaGFCITest(SpaClientDevice, SensorEntity):
    """Representation of the GFCI test result sensor."""

    def __init__(self, spaclient, config_entry):
        super().__init__(spaclient, config_entry)
        self._spaclient = spaclient
        self._icon = ICONS.get('GFCI Test')

    @property
    def unique_id(self) -> str:
        return f"{self._spaclient.get_macaddr().replace(':', '')}#gfci_test"

    @property
    def name(self):
        return 'GFCI Test'

    @property
    def icon(self):
        return self._icon

    @property
    def native_value(self):
        return self._spaclient.get_gfci_test_result()

    @property
    def entity_category(self):
        return EntityCategory.DIAGNOSTIC

    @property
    def available(self) -> bool:
        return self._spaclient.get_gateway_status()


class SpaModelName(SpaClientDevice, SensorEntity):
    """Representation of the spa model name sensor."""

    def __init__(self, spaclient, config_entry):
        super().__init__(spaclient, config_entry)
        self._spaclient = spaclient
        self._icon = ICONS.get('Model Name')

    @property
    def unique_id(self) -> str:
        return f"{self._spaclient.get_macaddr().replace(':', '')}#model_name"

    @property
    def name(self):
        return 'Model Name'

    @property
    def icon(self):
        return self._icon

    @property
    def native_value(self):
        return self._spaclient.get_model_name()

    @property
    def entity_category(self):
        return EntityCategory.DIAGNOSTIC

    @property
    def available(self) -> bool:
        return self._spaclient.get_gateway_status()


class SpaSoftwareVersion(SpaClientDevice, SensorEntity):
    """Representation of the spa software version sensor."""

    def __init__(self, spaclient, config_entry):
        super().__init__(spaclient, config_entry)
        self._spaclient = spaclient
        self._icon = ICONS.get('Software Version')

    @property
    def unique_id(self) -> str:
        return f"{self._spaclient.get_macaddr().replace(':', '')}#software_version"

    @property
    def name(self):
        return 'Software Version'

    @property
    def icon(self):
        return self._icon

    @property
    def native_value(self):
        return self._spaclient.get_ssid()

    @property
    def entity_category(self):
        return EntityCategory.DIAGNOSTIC

    @property
    def available(self) -> bool:
        return self._spaclient.get_gateway_status()


class SpaHeaterVoltage(SpaClientDevice, SensorEntity):
    """Representation of the heater voltage sensor."""

    def __init__(self, spaclient, config_entry):
        super().__init__(spaclient, config_entry)
        self._spaclient = spaclient
        self._icon = ICONS.get('Heater Voltage')

    @property
    def unique_id(self) -> str:
        return f"{self._spaclient.get_macaddr().replace(':', '')}#heater_voltage"

    @property
    def name(self):
        return 'Heater Voltage'

    @property
    def icon(self):
        return self._icon

    @property
    def native_value(self):
        return self._spaclient.get_info_heater_voltage()

    @property
    def entity_category(self):
        return EntityCategory.DIAGNOSTIC

    @property
    def available(self) -> bool:
        return self._spaclient.get_gateway_status()


class SpaHeaterType(SpaClientDevice, SensorEntity):
    """Representation of the heater type sensor."""

    def __init__(self, spaclient, config_entry):
        super().__init__(spaclient, config_entry)
        self._spaclient = spaclient
        self._icon = ICONS.get('Heater Type')

    @property
    def unique_id(self) -> str:
        return f"{self._spaclient.get_macaddr().replace(':', '')}#heater_type"

    @property
    def name(self):
        return 'Heater Type'

    @property
    def icon(self):
        return self._icon

    @property
    def native_value(self):
        return self._spaclient.get_info_heater_type()

    @property
    def entity_category(self):
        return EntityCategory.DIAGNOSTIC

    @property
    def available(self) -> bool:
        return self._spaclient.get_gateway_status()


class SpaConfigSignature(SpaClientDevice, SensorEntity):
    """Representation of the config signature sensor."""

    def __init__(self, spaclient, config_entry):
        super().__init__(spaclient, config_entry)
        self._spaclient = spaclient

    @property
    def unique_id(self) -> str:
        return f"{self._spaclient.get_macaddr().replace(':', '')}#config_signature"

    @property
    def name(self):
        return 'Config Signature'

    @property
    def icon(self):
        return "mdi:fingerprint"

    @property
    def native_value(self):
        return self._spaclient.get_info_cfg_sig()

    @property
    def entity_category(self):
        return EntityCategory.DIAGNOSTIC

    @property
    def available(self) -> bool:
        return self._spaclient.get_gateway_status()
