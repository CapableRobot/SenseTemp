##
## This MicroPython code is designed for the Adafruit HUZZAH ESP32.
## It fetches data from the Capable Robot Components SenseTemp 
## RTD Wing and prints temperatures (in C) it to the debug console.
##
## Temperature data is emitted at approximately 3 Hz.
##
## SenseTemp : https://www.crowdsupply.com/capable-robot-components/sensetemp
##

## MicroPython Imports
import time
import machine

## Local Imports
import adafruit_max31865 as max31865


RTD_NOMINAL   = 1000.0  ## Resistance of RTD at 0C
RTD_REFERENCE = 4300.0  ## Value of reference resistor on PCB

## Create Software SPI controller.  MAX31865 requires polarity of 0 and phase of 1.
## Currently, the micropython on the ESP32 does not support hardware SPI
sck  = machine.Pin( 5, machine.Pin.OUT)
mosi = machine.Pin(18, machine.Pin.IN)
miso = machine.Pin(19, machine.Pin.OUT)
spi  = machine.SPI(baudrate=50000, sck=sck, mosi=mosi, miso=miso, polarity=0, phase=1)

## Create SPI Chip Select pins
cs1  = machine.Pin(33, machine.Pin.OUT, value=1)
cs2  = machine.Pin(15, machine.Pin.OUT, value=1)
cs3  = machine.Pin(32, machine.Pin.OUT, value=1)
cs4  = machine.Pin(14, machine.Pin.OUT, value=1)
css  = [cs1, cs2, cs3, cs4]

sensors     = []
idx         = 0

## Create array of active RTD sensors and information about them
for cs in css:
    idx += 1

    sensors.append(
        max31865.MAX31865(
            spi, css[idx-1],
            wires        = 4,
            rtd_nominal  = RTD_NOMINAL,
            ref_resistor = RTD_REFERENCE)
    )

def timestamp():
    return float(time.ticks_ms()) / 1000.0

boot_time = timestamp()

while True:
    data = [timestamp() - boot_time] + [sensor.temperature for sensor in sensors]
    print(','.join(map(str,data)))
