
## MicroPython Imports
import time
import machine
import network
import ujson as json
from    _thread     import start_new_thread

## Local Imports
import adafruit_max31865 as max31865
import mqtt


def check_wifi(nic):
    if 'wifi-station' not in settings:
        return

    if nic.isconnected():
        return

    nic.connect(settings['wifi-station']['name'], settings['wifi-station']['pass'])

    while not nic.isconnected():
        time.sleep(0.2)

def mean(data):
    return sum(data)/float(len(data))

def _ss(data):
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def stddev(data, ddof=0):
    ss = _ss(data)
    pvar = ss/(len(data)-ddof)
    return pvar**0.5

def mqtt_thread():
    ## Create MQTT Connection
    c = mqtt.MQTTClient(settings['device']['name'], settings['mqtt']['ip'], 1883)
    c.connect()

    sensors     = []
    sensor_info = []
    idx         = 0

    ## Create array of active RTD sensors and information about them
    for location in settings['device']['sensors']:
        idx += 1

        if location.upper() == "DISABLE":
            continue

        sensors.append([
            idx,
            max31865.MAX31865(
                spi, css[idx-1],
                wires        = 4,
                rtd_nominal  = RTD_NOMINAL,
                ref_resistor = RTD_REFERENCE)
        ])

        sensor_info.append({
            "id"       : idx,
            "scale"    : settings['mqtt']['scale'],
            "type"     : "temperature",
            "sensor"   : "RTD1000 -> MAX31865",
            "location" : location
        })


    c.publish(settings['device']['name']+'/', json.dumps(sensor_info))

    while True:
        check_wifi(nic)

        meta    = []
        samples = []

        for idx, sensor in sensors:
            value = sensor.temperature*settings['mqtt']['scale']

            if settings['mqtt']['to_int']:
                value = int(value)

            meta.append({'id':idx, 'value' : value})
            samples.append(value)

        meta.append({'id':'agg','mean':mean(samples),'stddev':stddev(samples)})

        c.publish(settings['device']['name']+'/', json.dumps(meta))
        time.sleep(settings['mqtt']['sleep'])


settings = json.load(open("settings.json", 'r'))

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

## Setup WIFI Networking
if 'wifi-station' in settings:
    nic = network.WLAN(network.STA_IF)
    nic.active(True)
    check_wifi(nic)

## Become a MQTT client, if configured so
if 'mqtt' in settings:
    start_new_thread(mqtt_thread, ())



