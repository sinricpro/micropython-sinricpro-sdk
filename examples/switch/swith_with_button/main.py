from button import Button
from sinricpro import SinricPro 
from sinricpro.devices.sinricpro_switch import SinricProSwitch
from machine import Pin
import time

import uasyncio as a
import network

ssid = ""
ssid_password = ""
app_key    = ""
app_secret = ""
device_id  = ""

sinricpro = SinricPro()
sinricpro_switch = SinricProSwitch(device_id)

def button_change(button, event):
    global sinricpro_switch

    if event == Button.PRESSED:
        sinricpro_switch.send_power_state_event(state=True)
    if event == Button.RELEASED:
        sinricpro_switch.send_power_state_event(state=False)

button_one = Button(0, False, button_change)

async def handle_push_button_press():
    while True:
        button_one.update()
        await a.sleep_ms(0) # needed. otherwise other events won't fire!

async def on_disconnected():
    print('Disconnected from SinricPro...reboot?')

async def on_connected():
    print('Connected to SinricPro...')

# @timed_function
async def on_power_state_callback(device_id: str, state: bool):
    # Implement your logic to handle the power state change here
    print(f'device id: {device_id} state: {state}')
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
    global sinricpro_switch

    sinricpro.on_connected(on_connected)
    sinricpro.on_disconnected(on_disconnected)

    sinricpro_switch.on_power_state(on_power_state_callback)

    sinricpro.add_device(sinricpro_switch)
    sinricpro.start(app_key, app_secret, enable_log=True)

# main coroutine
async def main():
    do_wifi_connect()
    start_sinricpro()
    a.create_task(handle_push_button_press())

    while True:
        await a.sleep_ms(10_000)

# start asyncio task and loop
try:
    # start the main async tasks
    a.run(main())
finally:
    # reset and start a new event loop for the task scheduler
    a.new_event_loop()