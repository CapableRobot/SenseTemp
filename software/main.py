
## MicroPython Imports
import time
import machine
import network
import gc
import ujson as json
from    _thread     import start_new_thread

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

def wait_ap(ap):
    if ap.active() and ap.isconnected():
        print("AP Already Started")
        return

    while not ap.active() and not ap.isconnected():
        print('***')
        time.sleep(0.2)

    print("AP Now Started")

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
    c.publish(settings['device']['name']+'/', json.dumps(sensor_info))

    while True:
        check_wifi(nic)
        c.publish(settings['device']['name'], json.dumps(poll_sensors()))
        time.sleep(settings['mqtt']['sleep'])


settings = json.load(open("settings.json", 'r'))

RTD_NOMINAL   = 1000.0  ## Resistance of RTD at 0C
RTD_REFERENCE = 4300.0  ## Value of reference resistor on PCB
HTTP_HEADERS  = {"Access-Control-Allow-Origin": "*"}

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



## Setup WIFI Networking
if 'wifi-station' in settings:
    nic = network.WLAN(network.STA_IF)
    nic.active(True)
    check_wifi(nic)

if 'wifi-ap' in settings:
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=settings['wifi-ap']['name'])
    wait_ap(ap)

## Clean out allocated memory so far
gc.collect()
gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

## Become a MQTT client, if configured so
if 'mqtt' in settings:
    import mqtt
    start_new_thread(mqtt_thread, ())



def poll_sensors(extra_info=False):
    meta    = []
    samples = []

    for idx, sensor in sensors:
        value = sensor.temperature*settings['device']['scale']

        if settings['device']['to_int']:
            value = int(value)

        data = {'id':idx, 'value':value}

        if extra_info:
            data['name'] = sensor_info[idx-1]['name']

        meta.append(data)
        samples.append(value)

    meta.append({'id':'agg','mean':mean(samples),'stddev':stddev(samples)})
    return meta


def _acceptWebSocketCallback(webSocket, httpClient) :
    print("WS ACCEPT")
    webSocket.RecvTextCallback   = _recvTextCallback
    webSocket.RecvBinaryCallback = _recvBinaryCallback
    webSocket.ClosedCallback     = _closedCallback

def _recvTextCallback(webSocket, msg):
    print("WS RECV TEXT : %s" % msg)
    webSocket.SendText("Reply for %s" % msg)

def _recvBinaryCallback(webSocket, data):
    print("WS RECV DATA : %s" % data)

def _closedCallback(webSocket):
    print("WS CLOSED")

def _handle_datajson_get(httpClient, httpResponse, routeArgs=None):

    data = poll_sensors(extra_info=True)

    ## For convenience, add in:
    ##  each sensor's name (from the settings file)
    ##  and sensor global configuration (scale & int conversion)
    # for entry in data:
    #     if entry['id'] == 'agg':
    #         entry['scale']  = settings['device']['scale']
    #         entry['to_int'] = settings['device']['to_int']
    #     else:
    #         entry['name'] = sensor_info[entry['id']-1]['name']

    httpResponse.WriteResponseJSONOk(obj=data, headers=HTTP_HEADERS)

if 'http' in settings:
    from microWebSrv import MicroWebSrv

    handlers = [
      ( "/data.json", "GET", _handle_datajson_get ),
    ]

    mws = MicroWebSrv(routeHandlers=handlers, webPath='/www')
    mws.MaxWebSocketRecvLen     = 64     # Default is set to 1024
    mws.WebSocketThreaded       = False  # WebSockets without new threads
    mws.AcceptWebSocketCallback = _acceptWebSocketCallback

    ## Does not work, silently fails
    ## Might be due to attempting to start 10 threads
    # mws.Start()

    ## Works, but blocks the REPL
    mws.Start(threaded = False)

    ## Sometimes works
    # start_new_thread(mws._serverProcess, ())

