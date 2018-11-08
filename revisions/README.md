# SenseTemp Hardware Revisions

![SenseTemp PCB Image](../images/sensetemp_pcbs.jpg?raw=true)

* [CREAES](revisions/CREAES) : Last release 2018-10-18.
	* Changed from 0805 to 0603 passive components.
	* Moved all components to top side of PCB.
	* Added `USR` pin for user-controllable LED near the RTD connector.
	* Changed license from **CC BY-SA 4.0** to **CERN OHL v1.2**.
	* **IN PROGRESS** : Can be powered from either USB or Li-Ion sources.
* [X9EG](revisions/X9EG) : Released 2018-08-28.
	* Added `SIO` pin with AT21CS01 1-Wire EEPROM for configuration & serialization.
	* Added `EN` pin to allow host PCB to disable 5v to 3v regulator on this PCB.
	* Changed RTD connector from 20 pin (used on XTMT version) to 16 pin.
* [XTMT](revisions/XTMT) : Initial version released 2018-05-18.