<span align="center">

<a href="https://github.com/jozefnad/homeassistant-smartspaclient"><img src="https://raw.githubusercontent.com/jozefnad/homeassistant-smartspaclient/master/images/icon.png" width="150"></a>


# SmartSpa Client - Home Assistant custom component

</span>


**SmartSpa Client** for HomeAssistant is inspired by several similar projects and the work of many people.

If you find this integration useful, you can buy me a beer to help keep development going.

[![Buy me a beer](https://img.shields.io/badge/Donate-Buy%20me%20a%20beer-yellow?style=for-the-badge&logo=buy-me-a-coffee)](https://www.buymeacoffee.com/jozefnad)


## What you need

- A Hot Tub Equipped with a Balboa BP System
- SmartSpa W-Fi Module, bwa™ Wi-Fi Module (50350) or custom module with TCP port 4257
- Reference : http://www.balboawatergroup.com/bwa

## Installation

You can install this integration via [HACS](#hacs) or [manually](#manual).

### HACS

Search for the Spa Client integration and choose install. Reboot Home Assistant and configure the Spa Client integration via the integrations page or press the blue button below.

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=smartspaclient)


### Manual

Copy the `custom_components/smartspaclient` to your custom_components folder. Reboot Home Assistant and configure the SmartSpa Client integration via the integrations page or press the blue button below.

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=smartspaclient)


## Preview

<span align="center">

<a href="https://github.com/jozefnad/homeassistant-smartspaclient"><img src="https://raw.githubusercontent.com/jozefnad/homeassistant-smartspaclient/master/images/preview.png" width="500"></a>

<a href="https://github.com/jozefnad/homeassistant-smartspaclient"><img src="https://raw.githubusercontent.com/jozefnad/homeassistant-smartspaclient/master/images/options.png" width="400"></a>

</span>

Several elements have already been validated (with my spa), but several remain to be validated **with your help**. The following table shows what is known to be functional: 

### Climate & Temperature Control

Entity | Type | Tested | Programmed entity attributes
------ | ---- | ------ | ----------------------------
Spa Thermostat | Climate | ✓ | Heat Mode, Heating State, Standby Mode, Temp Range, Temperature Scale
Temperature Scale | Select | ✓ | Fahrenheit, Celsius
Clock Mode | Select | ✓ | 12 Hour, 24 Hour
Cleanup Cycle | Select | ✓ | Off, 30min, 60min, 90min, 120min, 150min, 180min, 240min

### Pumps & Jets

Entity | Type | Tested | Programmed entity attributes
------ | ---- | ------ | ----------------------------
Pump 1 | Switch | ✓ | Off, Low, High
Pump 2 | Switch | ✓ | Off, Low, High
Pump 3 | Switch | ✓ | Off, Low, High
Pump 4 | Switch | ? | Off, Low, High
Pump 5 | Switch | ? | Off, Low, High
Pump 6 | Switch | ? | Off, Low, High
Circulation Pump | Binary sensor | ✓ | False, True
Circulation Pump Status | Switch | ✓ | On/Off

### Heating System

Entity | Type | Tested | Programmed entity attributes
------ | ---- | ------ | ----------------------------
Heating State | Sensor | ✓ | Off, Heating, Heat Waiting
Heating | Binary sensor | ✓ | True (heating), False (idle/off)
Heat Mode | Switch | ✓ | Ready, Rest, Ready in Rest
Standby Mode | Switch | ✓ | On (disabled), Off (enabled)
Temperature Range | Switch | ✓ | Low, High

### Lights & Features

Entity | Type | Tested | Programmed entity attributes
------ | ---- | ------ | ----------------------------
Light 1 | Light | ✓ | On/Off, Brightness
Light 2 | Light | ? | On/Off, Brightness
Blower | Switch | ✓ | Off, On
Mister | Switch | ? | Off, On
Auxiliary 1 | Switch | ? | On/Off
Auxiliary 2 | Switch | ? | On/Off

### Filters & Schedules

Entity | Type | Tested | Programmed entity attributes
------ | ---- | ------ | ----------------------------
Filter Cycle 1 Status | Binary sensor | ✓ | Begins, Runs, Ends
Filter Cycle 1 Begins | Time | ✓ | N/A
Filter Cycle 1 Runs | Time | ✓ | N/A
Filter Cycle 2 Status | Binary sensor | ✓ | Begins, Runs, Ends
Filter Cycle 2 | Switch | ✓ | 0, 1
Filter Cycle 2 Begins | Time | ✓ | N/A
Filter Cycle 2 Runs | Time | ✓ | N/A

### System Status & Sensors

Entity | Type | Tested | Programmed entity attributes
------ | ---- | ------ | ----------------------------
Last Known Fault | Sensor | ✓ | Fault Code String
Spa State | Sensor | ✓ | Running, Initializing, Hold, Test
WiFi State | Sensor | ✓ | Connected, Connecting, Not Connected
Heating State | Sensor | ✓ | Off, Heating, Heat Waiting
Reminder | Sensor | ✓ | Reminder Type (Spa Needs Service, Filter Needs Cleaning, etc.)
Sensor A Temperature | Sensor | ✓ | Temperature (°F or °C)
Sensor B Temperature | Sensor | ✓ | Temperature (°F or °C)
GFCI Test | Sensor | ✓ | Pass/Fail Status
Model | Sensor | ✓ | Spa Model String
Software Version | Sensor | ✓ | Version Number
Heater Power | Sensor | ✓ | Power State

### System Controls & Settings

Entity | Type | Tested | Programmed entity attributes
------ | ---- | ------ | ----------------------------
Panel Lock | Switch | ✓ | On/Off (Locks front panel)
Settings Lock | Switch | ✓ | On/Off (Locks settings menu)
Reminders | Switch | ✓ | On/Off (Service reminders enabled)
M8 AI | Switch | ✓ | On/Off (AI features enabled)
Priming | Binary sensor | ✓ | True (priming), False (idle)
Notification | Binary sensor | ✓ | True (alarm active), False (no alarm)

Option | Tested
------ | ------
Entities polling rate (seconds) | Not yet implemented!
Time sync with Home Assistant | ✓

## Technical Documentation

### Protocol Overview
- **Communication Protocol:** Binary socket protocol on port 4257
- **Message Checksum:** CRC-8 validation (polynomial 0x07, initial value 0xb5, final XOR 0x02)
- **Status Updates:** 0x13 message type containing 28-32 bytes depending on spa model
- **Command Types:**
  - `0x11`: Toggle commands (pumps, lights, blower, etc.)
  - `0x27`: Preference updates (temperature scale, clock mode, cleanup cycle, reminders, M8 AI)
  - `0x2d`: Lock configuration (panel lock, settings lock)
  - `0x1d`: Standby mode control

### Entity Protocol Mapping

| Entity | Message Type | Parameter | Notes |
|--------|-------------|-----------|-------|
| Pumps 1-6, Lights, Blower, Mister, Aux | 0x11 | Toggle code | Direct on/off switching |
| Temperature Scale | 0x27 | [0x01, value] | 0=Fahrenheit, 1=Celsius |
| Clock Mode | 0x27 | [0x02, value] | 0=12hr, 1=24hr |
| Cleanup Cycle | 0x27 | [0x03, value] | 0=Off, 1-8=30-240min intervals |
| Reminders | 0x27 | [0x04, value] | Service reminder toggle |
| M8 AI | 0x27 | [0x05, value] | AI features toggle |
| Panel Lock | 0x2d | [0x01, value] | Locks front control panel |
| Settings Lock | 0x2d | [0x02, value] | Locks preference menu |
| Standby Mode | 0x1d | Toggle code | Master heating enable/disable |
| Heating State | 0x13 | Byte 10, bits 4-5 | 0=Off, 1=Heating, 2=Heat Waiting |
| Temperature Range | 0x13 | Byte 10, bit 2 | 0=Low (50-80°F), 1=High (80-104°F) |


### Configuration Flow
1. Connect to spa module on port 4257
2. Receive initial 0x13 status message
3. Parse all state variables and create Home Assistant entities
4. Maintain background read loop for status updates
5. Send keep-alive heartbeat every 30 seconds
6. Process user commands and send appropriate messages with CRC-8 validation

✓ = Tested and working properly  
? = Need your help to validate if this working properly (I don't have these options on my spa)

## Entity Statistics

- **Total Sensors:** 14 (Heating State, Spa State, WiFi State, Reminder, Sensor A/B Temps, GFCI Test, Model, Software, Heater Power, Last Known Fault, etc.)
- **Total Binary Sensors:** 5 (Priming, Heating, Notification, Circulation Pump, Filter Cycle Status)
- **Total Switches:** 10+ (Pumps 1-6, Lights 1-2, Blower, Mister, Heat Mode, Standby Mode, Temp Range, Filter Cycle 2, Circulation Pump, Panel Lock, Settings Lock, Reminders, M8 AI)
- **Total Select Entities:** 3 (Temperature Scale, Clock Mode, Cleanup Cycle)
- **Climate Entities:** 1 (Spa Thermostat with full HVAC control)
- **Light Entities:** 2 (Light 1, Light 2 with brightness control)
- **Time Entities:** 5 (Filter Cycle 1 Begin/Run times, Filter Cycle 2 Begin/Run times, plus schedule support)

## Key Features & Improvements

### Climate/Thermostat Control
- **Smart HVAC Mode:** Controlled by Standby Mode (OFF = heating disabled but pumps/filters continue, HEAT = heating enabled)
- **Heating State Monitoring:** Real-time tracking of heating status (Off, Heating, Heat Waiting)
- **Temperature Setpoint:** Full control of target water temperature
- **Unit Conversion:** Automatic handling of Fahrenheit/Celsius with Home Assistant configuration awareness
- **Extra Attributes:** Heat Mode preference, current heating state, temperature range, scale setting

### Preference Management (Climate Settings)
- **Temperature Scale:** Switch between Fahrenheit and Celsius
- **Clock Mode:** Toggle between 12-hour and 24-hour time format
- **Cleanup Cycle:** Set automatic cleanup intervals (Off, 30-240 minutes)
- **Reminders:** Enable/disable service reminder notifications
- **M8 AI:** Control AI-assisted features (where available)

### Security & Configuration
- **Panel Lock:** Prevent accidental button presses on spa control panel
- **Settings Lock:** Prevent unauthorized changes to spa settings

### Comprehensive Status Monitoring
- **Spa State Sensor:** Running, Initializing, Hold, or Test mode
- **WiFi State Sensor:** Real-time connection status monitoring
- **Heating State Sensor:** Detailed heating status (Off, Heating, Heat Waiting)
- **Reminder Sensor:** Active service reminders at a glance
- **GFCI Test Sensor:** Ground fault circuit interrupter status
- **Model & Version Info:** Spa model, software version, and heater power info
- **Temperature Sensors:** Separate sensors for Sensor A and B temperatures

### Reliability & Protocol Support
- **CRC-8 Validation:** All messages validated with proper checksum
- **Variable Message Lengths:** Support for different spa models with different message sizes
- **Async Socket Communication:** Non-blocking connection with keep-alive heartbeats
- **Automatic Reconnection:** Graceful handling of network interruptions
- **Message Queue:** Reliable command processing with proper synchronization

## Task List

### To do

- [ ] Autodiscovery via UDP broadcast of the module
- [ ] Numeric entity support for manual parameter adjustments
- [ ] Water level sensor support for future spa models
- [ ] UV system status monitoring

### Completed
- [x] Initial version
- [x] Complete entity 
- [x] Smart thermostat control via Standby Mode semantics
- [x] Preference management (Temperature Scale, Clock Mode, Cleanup Cycle)
- [x] System controls (Panel Lock, Settings Lock, Reminders, M8 AI)
- [x] Comprehensive status sensors (14 sensors covering all diagnostic data)
- [x] Binary sensors for key status flags (Priming, Heating, Notification, Circulation Pump)
- [x] Select entities for multi-option preferences
- [x] Device-aware entity grouping by platform
- [x] CRC-8 message validation with proper protocol implementation
- [x] Support for variable message lengths (different spa models)
- [x] Fixed heating state representation and climate thermostat logic
- [x] Fixed temperature scale command structure
- [x] Async socket lifecycle management with proper cleanup
