# SenseTemp

Designed by [Capable Robot Components](http://capablerobot.com).  
Follow us on [Twitter](http://twitter.com/capablerobot) for product announcements and updates.

---

**SenseTemp is available on [CrowdSupply](https://www.crowdsupply.com/capable-robot-components/sensetemp) & [Mouser](https://www.mouser.com/Search/Refine?Keyword=sensetemp).  Please visit the [campaign page](https://www.crowdsupply.com/capable-robot-components/sensetemp) or [Mouser](https://www.mouser.com/ProductDetail/Crowd-Supply/cs-sensetemp-01?qs=sGAEpiMZZMsSgQ5oX0A7uhzs7btMGoRQjdDbb5Xc%2F1l7fRq91ffQkQ%3D%3D) for product information and to purchase SenseTemp.** 

![SenseTemp PCB Image](images/sensetemp_pcbs.jpg?raw=true)

SenseTemp provides four highly accurate and flexible temperature sensors which allow you to understand the operation of your:

* Mobile robot
* Embedded system 
* Double pane windows on your house
* Home brewing operation
* Or any other system where temperature and thermal conduction is important

It's designed for quick tests as well as long-duration process monitoring.

## SenseTemp Features 

* **Small:** so that it can be on a mobile system being tested.  The RTDs themselves are 2 mm x 4 mm, making them thermally responsive and great for measurement of point heat sources
* **Inexpensive:** allowing many points of temperature monitoring
* **Battery Powered:** including LiPoly & USB power banks
* **Wireless:** to make test setup faster and more flexible
* **Open Software:** so that the device can directly feed data into a data logging system of your choice
* **Open Hardware:** to enable derivative designs and for easy hacking

## Specifications

|Feature|Specification|
|----|----|
|Sensors|4x Platinum resistance temperature detectors (RTDs)|
|RTD Accuracy|±0.15°C|
|Temperature Range|-50°C to 260°C|
|Interface ICs|4x [MAX31865](https://www.maximintegrated.com/en/products/sensors/MAX31865.html) with 4 wire sensing|
|Form Factor|[Adafruit Feather](https://www.adafruit.com/feather)|
|Dimensions|0.9" x 2.4"|

## Feather Hosts

SenseTemp is designed to mate with Adafruit Feather-compatible host modules, like:

* [Adafruit Feather M4 Express](https://www.adafruit.com/product/3857)
* [Adafruit Feather M0 Express](https://www.adafruit.com/product/3403)
* [Adafruit ESP32 Feather Host](https://www.adafruit.com/product/3405)
* [Adafruit HalloWing](https://www.adafruit.com/product/3900)

Note that the ES8266 Feather is **NOT** supported due to the limited IO on the ESP8266.  It does not have enough pins to support the four SPI devices of the SenseTemp.

## Software

The software running on the Feather host processor does change based on the feather host you are using.  This repository contains software for:

* [**CircuitPython:**](software-circuitpython) if you are using a Cortex M4 or M0 Feather.  
* [**MicroPython:**](software-micropython) if you are using an ESP32 Feather.  The ESP32 is not currently supported by CircuitPython.

## Hardware Revisions

* [CREAES](revisions/CREAES) : Last release 2018-10-18.
	* Changed from 0805 to 0603 passive components.
	* Moved all components to top side of PCB.
	* Changed license from **CC BY-SA 4.0** to **CERN OHL v1.2**.
	* Can be powered from either USB or Li-Ion sources.
* [X9EG](revisions/X9EG) : Released 2018-08-28.
	* Added `SIO` pin with AT21CS01 1-Wire EEPROM for configuration & serialization.
	* Added `EN` pin to allow host PCB to disable 5v to 3v regulator on this PCB.
	* Changed RTD connector from 20 pin (used on XTMT version) to 16 pin.
* [XTMT](revisions/XTMT) : Initial version released 2018-05-18.

## License Information

| **Type** | **License** |
| --- | --- |
| Hardware | Copyright Capable Robot Components 2018 <br><br>This documentation describes Open Hardware and is licensed under the [CERN OHL v1.2 or later](https://www.ohwr.org/licenses/cern-ohl/license_versions/v1.2). <br/><br/> You may redistribute and modify this documentation under the terms of the CERN OHL v.1.2.  This documentation is distributed WITHOUT ANY EXPRESS OR IMPLIED WARRANTY, INCLUDING OF MERCHANTABILITY, SATISFACTORY QUALITY AND FITNESS FOR A PARTICULAR PURPOSE. Please see the CERN OHL v.1.2 for applicable conditions |
| Software | [MIT License](LICENSE.txt) |
| Documentation | [Creative Commons Attribution-ShareAlike](https://creativecommons.org/licenses/by-sa/4.0/) License |

More detailed information about the CERN License is available in the [license](license) folder and on the [CERN website](https://www.ohwr.org/projects/cernohl/wiki).


| **OSHW Certification** |
| --- |
| ![OSHW Mark US000151](images/OSHW_mark_US000151.png?raw=true) | 
| [Certified open source hardware](https://certification.oshwa.org/us000151.html) by the [Open Source Hardware Association](https://www.oshwa.org) |
