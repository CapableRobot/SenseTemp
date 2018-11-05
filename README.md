# SenseTemp

Designed by [Capable Robot Components](http://capablerobot.com).  
Follow us on [Twitter](http://twitter.com/capablerobot) for product announcements and updates.

---

**SenseTemp is currently in-pre launch on CrowdSupply.  You can sign up on the [campaign page](https://www.crowdsupply.com/capable-robot-components/sensetemp) for project update.** 

This repository contains schematics, layout, and bill of materials for an [OSHW](https://www.oshwa.org/definition/) four channel RTD temperature sensor.  It is designed to mate with Adafruit Feather-compatible host modules, like:

* [Adafruit ESP32 Feather Host](https://www.adafruit.com/product/3405)
* [Adafruit HalloWing](https://www.adafruit.com/product/3900)

Note that the ES8266 Feather is **NOT** supported due to the limited IO on the ESP8266.  It does not have enough pins to support the four SPI devices of the SenseTemp.

## Software

The software running on the Feather host processor does change based on the feather host you are using.  This repository contains software for:

* [**CircuitPython:**](software-circuitpython) if you are using a Cortex M4 or M0 Feather.  
* [**MicroPython:**](software-micropython) if you are using an ESP32 Feather.  The ESP32 is not currently supported by CircuitPython.

tree/master/software-micropython

## Hardware Revisions

* [CREAES](revisions/CREAES) : Last release 2018-10-18.
	* Changed from 0805 to 0603 passive components.
	* Moved all components to top side of PCB.
	* Added `USR` pin for user-controllable LED near the RTD connector.
	* Changed license from **CC BY-SA 4.0** to **CERN OHL v1.2**.
* [X9EG](revisions/X9EG) : Released 2018-08-28.
	* Added `SIO` pin with AT21CS01 1-Wire EEPROM for configuration & serialization.
	* Added `EN` pin to allow host PCB to disable 5v to 3v regulator on this PCB.
	* Changed RTD connector from 20 pin (used on XTMT version) to 16 pin.
* [XTMT](revisions/XTMT) : Initial version released 2018-05-18.

## License Information

| **Type** | **License** |
| --- | --- |
| Hardware | Copyright Capable Robot Components 2018 <br><br>This documentation describes Open Hardware and is licensed under the [CERN OHL v1.2 or later](https://www.ohwr.org/licenses/cern-ohl/license_versions/v1.2). <br/><br/> You may redistribute and modify this documentation under the terms of the CERN OHL v.1.2.  This documentation is distributed WITHOUT ANY EXPRESS OR IMPLIED WARRANTY, INCLUDING OF MERCHANTABILITY, SATISFACTORY QUALITY AND FITNESS FOR A PARTICULAR PURPOSE. Please see the CERN OHL v.1.2 for applicable conditions |
| Software | [MIT License](tree/master/LICENSE.txt) |
| Documentation | [Creative Commons Attribution-ShareAlike](https://creativecommons.org/licenses/by-sa/4.0/) License |

More detailed information about the CERN License is available in the [license](license) folder and on the [CERN website](https://www.ohwr.org/projects/cernohl/wiki).


| **OSHW Certification** |
| --- |
| Coming Soon |

