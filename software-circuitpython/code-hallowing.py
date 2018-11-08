##
## This CircuitPython code is designed for the Adafruit HalloWing.
## It live-plots four RTD temperature sensors from Capable Robot Components
## SenseTemp RTD Wing onto the HalloWing LCD display.
##
## Written by Chris Osterwood during the 2018 Hackaday Supercon.
## Thanks to Adafruit for providing all attendees with HalloWings!
##
## HalloWing : https://www.adafruit.com/product/3900
## SenseTemp : https://www.crowdsupply.com/capable-robot-components/sensetemp
##

## CircuitPython Imports
import time

import board
import gc
import busio
import pulseio
import digitalio

## Local Imports
import adafruit_max31865 as max31865

from adafruit_rgb_display import color565
import adafruit_rgb_display.ST7735 as ST7735

DISPLAY_PX = 128

## These temperatures are in Fahrenheit
##
## They are used to draw scale lines on
## the LCD and to map Fahrenheit values to pixel positions.
TEMP_MIN  = 60
TEMP_MAX  = 100
TEMP_STEP = 10

def c_to_f(value):
    return float(value) * 9.0 / 5.0 + 32.0

def f_to_c(value):
    return (float(value) - 32.0) * 5.0 / 9.0

RTD_NOMINAL   = 1000.0  ## Resistance of RTD at 0C
RTD_REFERENCE = 4300.0  ## Value of reference resistor on PCB

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

## Create the ST7735 display and make it black
display = ST7735.ST7735R(spi,
    cs=digitalio.DigitalInOut(board.TFT_CS),
    dc=digitalio.DigitalInOut(board.TFT_DC),
    rst=digitalio.DigitalInOut(board.TFT_RESET)
)
display.fill(0)

## Create SPI Chip Select pins
cs1  = digitalio.DigitalInOut(board.D10)
cs2  = digitalio.DigitalInOut(board.D9)
cs3  = digitalio.DigitalInOut(board.D6)
cs4  = digitalio.DigitalInOut(board.D5)
css  = [cs1, cs2, cs3, cs4]

sensors = []

## Create array for the RTD sensors on the SenseTemp Wing
for cs in css:
    sensors.append(
        max31865.MAX31865(
            spi, cs,
            wires        = 4,
            rtd_nominal  = RTD_NOMINAL,
            ref_resistor = RTD_REFERENCE
        )
    )

## Turn on the HalloWing back-light
backlight = pulseio.PWMOut(board.TFT_BACKLIGHT)
backlight.duty_cycle = 50000


## Reference temperatures to draw on the LCD
temp_grid = [TEMP_MIN]
while temp_grid[-1] < TEMP_MAX:
    temp_grid.append(temp_grid[-1] + TEMP_STEP)

## Colors for the 4 RTD channels -> Red, Green, Blue, Purple
COLORMAP = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 0, 255)
]

## Determine vertical position for the temperature sample
def f_to_px(value):
    if value < TEMP_MIN:
        return 0

    if value > TEMP_MAX:
        return DISPLAY_PX-1

    px = (value - TEMP_MIN) * DISPLAY_PX / (TEMP_MAX - TEMP_MIN)
    return int(px)

## Re-draw the grid data at this position
def draw_grid_at_position(position):
    ## Clear all samples at this X position.
    display.vline(position, 0, DISPLAY_PX, color565(0,0,0))

    ## Draw white points at this X position
    ## to re-create the temperature scale
    for value in temp_grid:
        y = f_to_px(value)
        display.pixel(position, y, color565(255,255,255))

## Stores the last PX position for each temperature value
## this allows code to determine if new sample should be
## drawing with a point, or a line
last_px = [0,0,0,0]

def draw_temps_graph(position, data):
    draw_grid_at_position(position)

    for idx,value in enumerate(data):
        y     = f_to_px(c_to_f(value))
        dy    = abs(y - last_px[idx])
        color = color565(*COLORMAP[idx])

        if dy > 1:
            ypos = min(y, last_px[idx])
            display.vline(position, ypos, dy, color)
        else:
            display.pixel(position, y, color)

        last_px[idx] = y

gc.collect()

## Draw horizontal lines as a temperature scale
for value in temp_grid:
    y = f_to_px(value)
    display.hline(0, y, DISPLAY_PX, color565(255,255,255))

## Start on the left side of the screen
position = DISPLAY_PX

## Advance to the next PX position, read temperature data, draw it
while True:
    position -= 1

    data = [sensor.temperature for sensor in sensors]
    draw_temps_graph(position, data)

    ## We're at the end of the display, go back to the left side
    if position <= 0:
        position = DISPLAY_PX
