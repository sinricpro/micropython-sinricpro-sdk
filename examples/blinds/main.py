#   Example for how to use SinricPro Blind device

#   If you encounter any issues:
#   - visit https://github.com/sinricpro/micropython-sinricpro-sdk/issues and check for existing issues or open a new one

# To enable sdk debug output, add enable_log=True flag
# eg: sinricpro.start(app_key, app_secret, enable_log=True)

from sinricpro import SinricPro
from sinricpro.devices.sinricpro_blinds import SinricProBlinds
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
sinricpro_blinds = SinricProBlinds(device_id)

async def on_disconnected():
    print('Disconnected from SinricPro...reboot?')

async def on_connected():
    print('Connected to SinricPro...')

# @timed_function
async def on_power_state_callback(device_id: str, state: bool)->bool:
    print(f'device id: {device_id} state: {state}')
    return True

# @timed_function
async def on_range_value_callback(device_id: str, range_value: int)->bool:
    print(f'device id: {device_id}, change fan speed to: {range_value}')
    return True

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
    global sinricpro_blinds

    sinricpro.on_connected(on_connected)
    sinricpro.on_disconnected(on_disconnected)
    sinricpro_blinds.on_power_state(on_power_state_callback)
    sinricpro_blinds.on_range_value(on_range_value_callback)

    sinricpro.add_device(sinricpro_blinds)
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
