#   Example for how to control a relay connected to GPIO 26 and also a use a push button connected to GPIO 0 to turn on/off

#   If you encounter any issues:
#   - visit https://github.com/sinricpro/micropython-sinricpro-sdk/issues and check for existing issues or open a new one

# To enable sdk debug output, add enable_log=True flag
# eg: sinricpro.start(app_key, app_secret, enable_log=True)

from button import Button
from sinricpro import SinricPro 
from sinricpro.devices.sinricpro_switch import SinricProSwitch
from machine import Pin

import uasyncio as a
import network

ssid = ""
ssid_password = ""
app_key    = ""
app_secret = ""
device_id  = ""

# relay is connected to GPIO 26
relay = Pin(26, Pin.OUT)

sinricpro = SinricPro()
sinricpro_switch = SinricProSwitch(device_id)

is_powered_on = False

# gets called button pushed
def button_change(button, event):
    global sinricpro_switch
    global is_powered_on

    if event == Button.RELEASED:
        is_powered_on = not is_powered_on # invert the current state
        if is_powered_on:
            relay.value(1) # turn on relay
        else:
            relay.value(0) # turn off relay

        sinricpro_switch.send_power_state_event(state=is_powered_on)

# push button is connected to GPIO 0
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

    if state:
        relay.value(1)
    else:
        relay.value(0)

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
    sinricpro.start(app_key, app_secret)

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