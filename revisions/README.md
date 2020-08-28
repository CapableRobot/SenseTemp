# SenseTemp Hardware Revisions

Designed by [Capable Robot Components](http://capablerobot.com).  
Follow us on [Twitter](http://twitter.com/capablerobot) for product announcements and updates.

---

**SenseTemp is available on [CrowdSupply](https://www.crowdsupply.com/capable-robot-components/sensetemp) & [Mouser](https://www.mouser.com/Search/Refine?Keyword=sensetemp).  Please visit the [campaign page](https://www.crowdsupply.com/capable-robot-components/sensetemp) or [Mouser](https://www.mouser.com/ProductDetail/Crowd-Supply/cs-sensetemp-01?qs=sGAEpiMZZMsSgQ5oX0A7uhzs7btMGoRQjdDbb5Xc%2F1l7fRq91ffQkQ%3D%3D) for product information and to purchase SenseTemp.** 

![SenseTemp PCB Image](../images/sensetemp_pcbs.jpg?raw=true)

---

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

---

Also in this folder are two adapter PCBs which allows SenseTemp's 50mil (4x 4-wire) connector to be adapted to 4x 2-way 5mm screw terminals, allowing SenseTemp to use 2-wire and 3-wire (in 2-wire mode) P1000 RTDs.

The 'stacking' design has the same outline and mounting as SenseTemp and is designed to stack vertically above SenseTemp using a [AMP Minitek 20021321-00016C4LF](https://octopart.com/20021321-00016c4lf-amphenol+icc+%2F+fci-12642443?r=sp) (or similar) connector.

The 'cabled' design is smaller and cabled to SenseTemp via a 16 conductor, 50 mil ribbon cabled.  The recommended 16 pin connector for it is [CNC Tech 3221-16-0300-00](https://octopart.com/3221-16-0300-00-cnc+tech-47114357?r=sp) or similar.

Bare PCBs (e.g. no components installed or included) are available for purchase directly from OSHPark:

| [Cabled Adapter](https://oshpark.com/shared_projects/WjlpBAlQ) | [Stacking Adapter](https://oshpark.com/shared_projects/11pGTiwa) |
|---|---|
|[![Cabled Adapter Image](../images/cabled_adapter.png?raw=true)](https://oshpark.com/shared_projects/WjlpBAlQ)| [![Stacking Adapter Image](../images/stacking_adapter.png?raw=true)](https://oshpark.com/shared_projects/11pGTiwa) |

---