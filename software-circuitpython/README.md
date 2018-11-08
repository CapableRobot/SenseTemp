# SenseTemp with CircuitPython

Designed by [Capable Robot Components](http://capablerobot.com).  
Follow us on [Twitter](http://twitter.com/capablerobot) for product announcements and updates.

---

**SenseTemp is currently in-pre launch on CrowdSupply.  You can sign up on the [campaign page](https://www.crowdsupply.com/capable-robot-components/sensetemp) for project update.** 

---

During the [2018 Hackaday Supercon](https://hackaday.io/superconference/), Adafruit donated HalloWing badges to the attendees and I wrote the CiruitPython code released here, which graphs temperatures from SenseTemp on the HalloWing LCD.  

|![Hallowing displaying temperature data from SenseTemp](../images/hallowing_front.jpg?raw=true)|![SenseTemp installed into HalloWing Feather socket](../images/hallowing_rear.jpg?raw=true)|
|:---:|:---:|
|HalloWing showing a time-history graph of the four temperature sensors.  Vertical scale is 60F to 100F.| Rear of HallowWing, showing SenseTemp board installed|

The full code is in `code-hallowing.py`, which should be renamed `code.py` so that it is auto-run by CircuitPython.

The main part of the display routine is shown here:

```python
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

    ## Draw white grid lines at this X position
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
```

Nearly any Feather Host running CircuitPython will support SenseTemp.  The only exception known to date is the ESP8266 Host as it does not have enough IO pins for the 4 SPI chip select pins.