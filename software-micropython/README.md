# MicroPython SenseTemp

Designed by [Capable Robot Components](http://capablerobot.com).  Follow us on [Twitter](http://twitter.com/capablerobot) for product announcements and updates.

---

This folder contains MicroPython software for use of the SenseTemp with the [Adafruit ESP32 Feather Host](https://www.adafruit.com/product/3405).

## Installation

1. Install tools

```
pip3 install esptool adafruit-ampy
```

2. Flash MicroPython onto the device

```
espefuse.py --port /dev/ttyUSB1 set_flash_voltage 3.3V
esptool.py --chip esp32 erase_flash
esptool.py --chip esp32 --port /dev/ttyUSB1 write_flash -z 0x1000 ../firmware/esp32-20180511-v1.9.4.bin
```

The first command is necessary if the SenseTemp PCB has been soldered to the ESP32 module, due to the PCB pulling up GPIO12 (the SIO pin).

By default, the ESP32 sees that as a signal to provide the flash chip with 1.8v instead of the default 3.3v.  This causes the SPI flash to brown out during writing and the MD5 checksum verify step will fail (because the flash is corrupted).  Setting the EFUSE causes the ESP32 to ignore the GPIO12 pin and always provide 3.3v to the SPI flash.

3. Load MicroPython source files.  Due the size of the www folder, this will take a while.  Be patient.

```
ampy put lib
ampy put www
ampy put settings.json
ampy put main.py
```


## Development

During development, it's best to load the main file under a different name so that the firmware does not automatically execute it.  

If the MicroPython code hangs, the ampy tool has a hard time putting the ESP32 module into raw communication mode (wherein it can upload files).  These commands can be used to 

1. Upload the in-development main.py file
2. Open a serial console (you will need to change the path) to the MicroPython REPL.
3. Start the in-development software.  Errors will be printed to the REPL.

```
ampy put main.py tmp.py
screen /dev/ttyUSB1 115200
> from tmp import *
```


