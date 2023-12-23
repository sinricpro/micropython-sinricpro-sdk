
# Light

from sinricpro import SinricPro
from sinricpro.devices.sinricpro_light import SinricProLight
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
sinricpro_light = SinricProLight(device_id)

async def on_power_state_callback(device_id: str, state: bool) -> bool:
    print(f'device id: {device_id} state: {state}')
    return True

async def on_brightness_callback(device_id: str, brightness: int) -> bool:
    print(f'device id: {device_id} brightness: {brightness}')
    return True

async def on_adjust_brightness_callback(device_id: str, brightness_delta: int) -> bool:
    print(f'device id: {device_id} adjust brightness by: {brightness_delta}')
    return True

async def on_color_callback(device_id: str, r: int, g: int, b: int) -> bool:
    print(f'device id: {device_id} color changed to r:{r},g:{g},b:{b}')
    return True

async def on_color_temperature_callback(device_id: str, color_temperature: int) -> bool:
    print(f'device id: {device_id} color temperature changed to {color_temperature}')
    return True

async def on_increase_color_temperature_callback(device_id: str) -> bool:
    print(f'device id: {device_id} increase color temperature')
    return True

async def on_decrease_color_temperature_callback(device_id: str) -> bool:
    print(f'device id: {device_id} decrease color temperature')
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
    global sinricpro_light

    sinricpro_light.on_power_state(on_power_state_callback)
    sinricpro_light.on_brightness(on_brightness_callback)
    sinricpro_light.on_adjust_brightness(on_adjust_brightness_callback)
    sinricpro_light.on_color(on_color_callback)
    sinricpro_light.on_color_temperature(on_color_temperature_callback)
    sinricpro_light.on_increase_color_temperature(on_increase_color_temperature_callback)
    sinricpro_light.on_decrease_color_temperature(on_decrease_color_temperature_callback)

    sinricpro.add_device(sinricpro_light)
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
