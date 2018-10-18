Here we are compiling a community changelog.

If you come up with a modification of our designs, please share it
with the community, log your changes below, and upload the files to
our GitHub repository.

# Change Format

**NAME** on DATE by *Your name*.
Description of modification

# Change Log

* **[CREAES](https://github.com/CapableRobot/SenseTemp/tree/master/revisions/CREAES)** on 2018-10-18 by *Chris Osterwood*
	* Changed from 0805 to 0603 passive components.
	* Moved all components to top side of PCB.
	* Added `USR` pin for user-controllable LED near the RTD connector.
	* Changed license from **CC BY-SA 4.0** to **CERN OHL v1.2**.
* **[X9EG](https://github.com/CapableRobot/SenseTemp/tree/master/revisions/X9EG)** on 2018-08-28 by *Chris Osterwood*
	* Added `SIO` pin with AT21CS01 1-Wire EEPROM for configuration & serialization.
	* Added `EN` pin to allow host PCB to disable 5v to 3v regulator on this PCB.
	* Changed RTD connector from 20 pin (used on XTMT version) to 16 pin.
* **[XTMT](https://github.com/CapableRobot/SenseTemp/tree/master/revisions/XTMT)** 2018-05-18 by *Chris Osterwood*