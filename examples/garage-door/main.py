#   Example for how to use SinricPro Garage Door

#   If you encounter any issues:
#   - visit https://github.com/sinricpro/micropython-sinricpro-sdk/issues and check for existing issues or open a new one

# To enable sdk debug output, add enable_log=True flag
# eg: sinricpro.start(app_key, app_secret, enable_log=True)

from sinricpro import SinricPro
from sinricpro.devices.sinricpro_garagedoor import SinricProGarageDoor
from sinricpro.utils.timed_func import timed_function

import uasyncio as a 
import network

# enter wifi details
ssid = ""
ssid_password = ""

# get these from https://portal.sinric.pro
app_key    = ""
app_secret = ""
device_id  = ""

sinricpro = SinricPro()
sinricpro_garage_door = SinricProGarageDoor(device_id)

async def on_disconnected():
    print('Disconnected from SinricPro...reboot?')

async def on_connected():
    print('Connected to SinricPro...')

# @timed_function
async def on_set_mode_callback(device_id: str, mode: str):
    print(f'device id: {device_id}, mode: {mode}')
    return True

# call this method when you want to update on physical change (eg via push-button)
def when_door_open_or_closed(open: bool)->None:
    print(f'Door state changed to: {open}')
    global sinricpro_garage_door
    newState = "Open" if open else "Close"
    sinricpro_garage_door.send_mode_event(newState) # can be "Close" or "Open"

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
    global sinricpro_garage_door

    sinricpro.on_connected(on_connected)
    sinricpro.on_disconnected(on_disconnected)
    sinricpro_garage_door.on_set_mode(on_set_mode_callback)
    sinricpro.add_device(sinricpro_garage_door)
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
