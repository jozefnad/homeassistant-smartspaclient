<span align="center">

<a href="https://github.com/jozefnad/homeassistant-smartspaclient"><img src="https://raw.githubusercontent.com/jozefnad/homeassistant-smartspaclient/master/images/icon.png" width="150"></a>


# SmartSpa Client - Home Assistant custom component

</span>


**SmartSpa Client** for HomeAssistant is inspired by several similar projects and the work of many people.

## What you need

- A Hot Tub Equipped with a Balboa BP System
- smartspa module, bwa™ Wi-Fi Module (50350) or custom module which emulates the bwa™ Wi-Fi Module on TCP port 4257

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

Entity | Type | Tested | Programmed entity attributes
------ | ---- | ------ | ----------------------------
Auxiliary 1 | Switch | ? | N/A
Auxiliary 2 | Switch | ? | N/A
Blower | Switch | ✓ | Off, On
Circulation Pump | Binary sensor | ✓ | False, True
Filter Cycle 1 Begins | Time | ✓ | N/A
Filter Cycle 1 Runs | Time | ✓ | N/A
Filter Cycle 1 Status | Binary sensor | ✓ | Begins, Runs, Ends
Filter Cycle 2 | Switch | ✓ | 0, 1
Filter Cycle 2 Begins | Time | ✓ | N/A
Filter Cycle 2 Runs | Time | ✓ | N/A
Filter Cycle 2 Status | Binary sensor | ✓ | Begins, Runs, Ends
Heat Mode | Switch | ✓ | Ready, Rest, Ready in Rest
Hold Mode | Switch | ✓ | Remaining Time
Last Known Fault | Sensor | ✓ | N/A
Light 1 | Light | ✓ | False, True
Light 2 | Light | ? | False, True
Mister | Switch | ? | Off, On
Pump 1 | Switch | ✓ | Off, Low, High
Pump 2 | Switch | ✓ | Off, Low, High
Pump 3 | Switch | ✓ | Off, Low, High
Pump 4 | Switch | ? | Off, Low, High
Pump 5 | Switch | ? | Off, Low, High
Pump 6 | Switch | ? | Off, Low, High
Spa Thermostat | Climate | ✓ | N/A
Standby Mode | Switch | ✓ | N/A
Temperature Range | Switch | ✓ | Low, High

Option | Tested
------ | ------
Entities polling rate (seconds) | Not yet implemented!
Time sync with Home Assistant | ✓

✓ = Tested and working properly  
? = Need your help to validate if this working properly (I don't have these options on my spa)

## Task List

### To do

- [ ] Autodiscovery via UDP broadcast of the module

### Completed
- [x] Initial version

## Inspiration / Credits

- https://github.com/plmilord/Hass.io-custom-component-spaclient | Forked project, initial inspiration!
- https://github.com/ccutrer/balboa_worldwide_app/wiki | Detailed Wiki on bwa protocol.
- https://github.com/garbled1/pybalboa | Main program in Python to interface the bwa module. Source of the CRC function. Very well programmed and documented!
- https://github.com/garbled1/balboa_homeassistan | Balboa Spa Client integration for Home Assistant which sit on previous ```pybalboa``` main program.

