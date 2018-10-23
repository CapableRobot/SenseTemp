# SenseTemp

Designed by [Capable Robot Components](http://capablerobot.com).  Follow us on [Twitter](http://twitter.com/capablerobot) for product announcements and updates.

---

This repository contains schematics, layout, and bill of materials for an [OSHW](https://www.oshwa.org/definition/) four channel RTD temperature sensor.  It is designed to mate with Adafruit Feather-compatible host modules, like their [ESP32 Feather Host](https://www.adafruit.com/product/3405).

## Installation

1. Install tools

```
pip3 install esptool adafruit-ampy
```

2. Flash MicroPython onto the device

```
espefuse.py --port /dev/ttyUSB1 set_flash_voltage 3.3V
esptool.py --chip esp32 erase_flash
esptool.py --chip esp32 --port /dev/ttyUSB1 write_flash -z 0x1000 firmware/esp32-20180511-v1.9.4.bin
```

The first command is necessary if the SenseTemp PCB has been soldered to the ESP32 module, due to the PCB pulling up GPIO12 (the SIO pin).

By default, the ESP32 sees that as a signal to provide the flash chip with 1.8v instead of the default 3.3v.  This causes the SPI flash to brown out during writing and the MD5 checksum verify step will fail (because the flash is corrupted).  Setting the EFUSE causes the ESP32 to ignore the GPIO12 pin and always provide 3.3v to the SPI flash.

3. Load MicroPython source files

```
ampy put lib
ampy put www
ampy put settings.json
ampy put main.py
```


## Development

During development, it's best to load the main file under a different name so that the firmware does not automatically execute it.

```
ampy put main.py tmp.py
screen /dev/ttyUSB1 115200
> from tmp import *
```

## Revisions

* [CREAES](tree/master/revisions/CREAES) : Release 2018-10-18.
	* Changed from 0805 to 0603 passive components.
	* Moved all components to top side of PCB.
	* Added `USR` pin for user-controllable LED near the RTD connector.
	* Changed license from **CC BY-SA 4.0** to **CERN OHL v1.2**.
* [X9EG](tree/master/revisions/X9EG) : Released 2018-08-28.
	* Added `SIO` pin with AT21CS01 1-Wire EEPROM for configuration & serialization.
	* Added `EN` pin to allow host PCB to disable 5v to 3v regulator on this PCB.
	* Changed RTD connector from 20 pin (used on XTMT version) to 16 pin.
* [XTMT](tree/master/revisions/XTMT) : Initial version released 2018-05-18.

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

