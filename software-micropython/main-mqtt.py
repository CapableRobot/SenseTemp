
## MicroPython Imports
import time
import machine
import network
import gc
import ujson as json
import mqtt

## Local Imports
import adafruit_max31865 as max31865

def check_wifi(nic):
    if 'wifi-station' not in settings:
        return

    if nic.isconnected():
        return

    nic.connect(settings['wifi-station']['name'], settings['wifi-station']['pass'])

    while not nic.isconnected():
        time.sleep(0.2)

def poll_sensors(extra_info=False):
    samples = []

    for idx, sensor in sensors:
        value = sensor.temperature*settings['device']['scale']

        if settings['device']['to_int']:
            value = int(value)

        samples.append([sensor_info[idx-1]['name'],value])

    return samples

def format_data(data):
    return "\n".join(s[0]+","+str(s[1]) for s in data)    

settings = json.load(open("settings-mqtt.json", 'r'))

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
sensor_info = []
idx         = 0

## Create array of active RTD sensors and information about them
for name in settings['device']['sensors']:
    idx += 1

    if name.upper() == "DISABLE":
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
        "scale"    : settings['device']['scale'],
        "type"     : "temperature",
        "sensor"   : "RTD1000 -> MAX31865",
        "name"     : name
    })

print("WIFI : Connecting ....")

## Setup WIFI Networking as a client
if 'wifi-station' in settings:
    nic = network.WLAN(network.STA_IF)
    nic.active(True)
    check_wifi(nic)

print("WIFI : Connected ")

## Clean out allocated memory so far
gc.collect()
gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

## Create MQTT Connection
c = mqtt.MQTTClient(
    client_id = settings['device']['name'], 
    server    = settings['mqtt']['server'], 
    user      = settings['mqtt']['user'],
    password  = settings['mqtt']['key'],

    ssl=False
)

print("MQTT Client : Created")

c.connect()
print("MQTT Client : Connected")

# Publish temperatures to Adafruit IO using MQTT
#
# Format of feed name:  
#   "ADAFRUIT_USERNAME/groups/ADAFRUIT_IO_GROUPNAME"
mqtt_feedname = bytes('{:s}/groups/{:s}/csv'.format(settings['mqtt']['user'], settings['mqtt']['feed']), 'utf-8')

while True:
    check_wifi(nic)

    # Multiple topics can be published with one message if the CSV form is used:
    #   SENSORNAME1,VALUE1
    #   SENSORNAME1,VALUE2
    #
    # `poll_sensors` returns [[name1,value1],[name2,value2],...] formatted data
    # `format_data` transforms that data into this CSV string form
    #
    # Measurements will appear as
    #   USERNAME/feeds/FEEDNAME.SENSORNAME1
    #   USERNAME/feeds/FEEDNAME.SENSORNAME2
    #   USERNAME/feeds/FEEDNAME.SENSORNAME3
    #   USERNAME/feeds/FEEDNAME.SENSORNAME4
    #
    # where the following are specified in the settings JSON file:
    #   FEEDNAME is settings['mqtt']['feed']
    #   SENSORNAME_ is the settings['device']['sensors'] array
    c.publish(mqtt_feedname, format_data(poll_sensors()))

    time.sleep(settings['mqtt']['sleep'])
    gc.collect()