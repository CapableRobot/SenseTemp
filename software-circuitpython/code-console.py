##
## This CircuitPython code is designed for the Adafruit Feather M0 & M4.
## It fetches data from the Capable Robot Components SenseTemp 
## RTD Wing and prints temperatures (in C) it to the debug console.
##
## Temperature data is emitted at approximately 3 Hz.
##
## SenseTemp : https://www.crowdsupply.com/capable-robot-components/sensetemp
##

## CircuitPython Imports
import digitalio
import busio

import board
import time

## Local Imports
import adafruit_max31865 as max31865

RTD_NOMINAL   = 1000.0  ## Resistance of RTD at 0C
RTD_REFERENCE = 4300.0  ## Value of reference resistor on PCB

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

## Create SPI Chip Select pins
cs1  = digitalio.DigitalInOut(board.D10)
cs2  = digitalio.DigitalInOut(board.D9)
cs3  = digitalio.DigitalInOut(board.D6)
cs4  = digitalio.DigitalInOut(board.D5)
css  = [cs1, cs2, cs3, cs4]

sensors = []

## Create array for the RTD sensors on the SenseTemp Wing
for cs in css:
    cs.switch_to_output(digitalio.DriveMode.PUSH_PULL)

    sensors.append(
        max31865.MAX31865(
            spi, cs,
            wires        = 4,
            rtd_nominal  = RTD_NOMINAL,
            ref_resistor = RTD_REFERENCE
        )
    )

boot_time = time.monotonic()

while True:
    data = [sensor.temperature for sensor in sensors]
    print(time.monotonic() - boot_time, data)
