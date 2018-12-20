##
## This CircuitPython code is designed for the Adafruit Feather M0 & M4.
## It fetches data from the Capable Robot Components SenseTemp 
## RTD Wing and prints temperatures (in C) it to the debug console.
##
## It also prints temperatures (in F) and time since boot to an attached
## OLED 128x32 screen, like the one on the Adafruit FeatherWing OLED
##
## Temperature data is emitted at approximately 3 Hz.
##
## SenseTemp : https://www.crowdsupply.com/capable-robot-components/sensetemp
## FeatherWing OLED : https://www.adafruit.com/product/2900
##

## CircuitPython Imports
import digitalio
import busio

import board
import time

## Local Imports
import neopixel
import adafruit_max31865 as max31865
import adafruit_ssd1306 as ssd1306

def c_to_f(c):
    return c*1.8 + 32.0

RTD_NOMINAL   = 1000.0  ## Resistance of RTD at 0C
RTD_REFERENCE = 4300.0  ## Value of reference resistor on PCB

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
i2c = busio.I2C(board.SCL, board.SDA)

oled = ssd1306.SSD1306_I2C(128, 32, i2c)

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
    now  = time.monotonic() - boot_time
    print(now, data)

    oled.fill(0)
    oled.text("SenseTemp {0:6.1f}".format(now), 0, 0)
    oled.text('1 {0:0.1f}F'.format(c_to_f(data[0])), 0, 10)
    oled.text('2 {0:0.1f}F'.format(c_to_f(data[1])), 72, 10)
    oled.text('3 {0:0.1f}F'.format(c_to_f(data[2])), 0, 20)
    oled.text('4 {0:0.1f}F'.format(c_to_f(data[3])), 72, 20)
    oled.show()