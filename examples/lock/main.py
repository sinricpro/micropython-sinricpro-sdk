# Lock

from sinricpro import SinricPro
from sinricpro.devices.sinricpro_lock import SinricProLock
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
sinricpro_lock = SinricProLock(device_id)

async def on_disconnected():
    print('Disconnected from SinricPro...reboot?')

async def on_connected():
    print('Connected to SinricPro...')

async def on_lock_state_callback(device_id: str, state: bool) -> bool:
    print(f'device id: {device_id} state: {state}')
    return True

# call this method when you want to update on physical change (eg via push-button)
def lock_state_changed(locked: bool)->None:
    print(f'Locked state changed to: {locked}')
    global sinricpro_lock
    sinricpro_lock.send_lock_state_event(locked)

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
    global sinricpro_lock

    sinricpro.on_connected(on_connected)
    sinricpro.on_disconnected(on_disconnected)
    sinricpro_lock.on_lock_state(on_lock_state_callback)

    sinricpro.add_device(sinricpro_lock)
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
