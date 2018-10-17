# Feather-RTD

## Installation

* Install tools

```
pip3 install esptool adafruit-ampy
```

* Flash MicroPython onto the device

```
espefuse.py --port /dev/ttyUSB1 set_flash_voltage 3.3V
esptool.py --chip esp32 erase_flash
esptool.py --chip esp32 --port /dev/ttyUSB1 write_flash -z 0x1000 firmware/esp32-20180511-v1.9.4.bin
```

The first command is necessary if the Feather-RTD wing has been soldered to the ESP32 module, due to the wing pulling up GPIO12 (the SIO pin).

By default, the ESP32 sees that as a signal to provide the flash chip with 1.8v instead of the default 3.3v.  This causes the SPI flash to brown out during writing and the MD5 checksum verify step will fail (because the flash is corrupted).  Setting the EFUSE causes the ESP32 to ignore the GPIO12 pin and always provide 3.3v to the SPI flash.

* Load MicroPython source files


## Development

During development, its' best to load the main file under a different name so that the firmware does not automatically execute it.

```
ampy put main.py tmp.py
screen /dev/ttyUSB1 115200
> from tmp import *
```