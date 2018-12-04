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

import neopixel

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
pixel = False

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

if hasattr(board, 'NEOPIXEL'):
    led = neopixel.NeoPixel(board.NEOPIXEL, 1)
    led.brightness = 0.3
    pixel = True

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0:
        return 0, 0, 0

    if pos > 255:
        return 255, 0, 0

    if pos < 85:
        return int(255 - pos * 3), int(pos * 3), 0

    if pos < 170:
        pos -= 85
        return 0, int(255 - pos * 3), int(pos * 3)

    pos -= 170
    return int(pos * 3), 0, int(255 - (pos * 3))


while True:
    data = [sensor.temperature for sensor in sensors]
    print(time.monotonic() - boot_time, data)

    if pixel:
        # Scale and reverse colors so that high temperatures (30C) -> red color
        color = 255 - data[0]*7
        led.fill(wheel(int(color)))
