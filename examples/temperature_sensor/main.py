# TemperatureSensor

from sinricpro import SinricPro
from sinricpro.devices.sinricpro_temperature_sensor import SinricProTemperatureSensor
from sinricpro.utils.timed_func import timed_function

import uasyncio as a 
import network

# enter wifi details
ssid = ""
ssid_password = ""

# get from https://portal.sinric.pro
app_key    = ""
app_secret = ""
device_id  = ""

sinricpro = SinricPro()
sinricpro_temperature_sensor = SinricProTemperatureSensor(device_id)

# call this method when you want to update temperature and humidity on server
def update_temperature(temperature: float, humidity: float = -1)->None:
    global sinricpro_temperature_sensor
    sinricpro_temperature_sensor.send_temperature_event(temperature, humidity)

# connect to wifi
# @timed_function
def do_wifi_connect():
    sta_if = network.WLAN(network.STA_IF)
    ap = network.WLAN(network.AP_IF) # create access-point interface
    ap.active(False)         # deactivate the interface
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, ssid_password)
        while not sta_if.isconnected():
            pass
    print('Connected network config:', sta_if.ifconfig())

# start sinricpro
def start_sinricpro():
    global sinricpro
    global sinricpro_temperature_sensor

    sinricpro.add_device(sinricpro_temperature_sensor)
    sinricpro.start(app_key, app_secret)

# main coroutine
async def main():
    do_wifi_connect()
    start_sinricpro()

    while True:
        await a.sleep_ms(10_000)

# start asyncio task and loop
try:
    # start the main async tasks
    a.run(main())
finally:
    # reset and start a new event loop for the task scheduler
    a.new_event_loop()
