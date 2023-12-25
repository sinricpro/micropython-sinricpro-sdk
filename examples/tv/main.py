# TV

from sinricpro import SinricPro
from sinricpro.devices.sinricpro_tv import SinricProTV
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
sinricpro_tv = SinricProTV(device_id)

async def on_disconnected():
    print('Disconnected from SinricPro...reboot?')

async def on_connected():
    print('Connected to SinricPro...')

# @timed_function
async def on_power_state_callback(device_id: str, state: str)->bool:
    print(f'device id: {device_id} state: {state}')
    return True

# @timed_function
async def on_mute_callback(device_id: str, mute: bool)->bool:
    print(f'device id: {device_id} mute: {mute}')
    return True

# @timed_function
async def on_set_volume_callback(device_id: str, volume: int)->bool:
    print(f'device id: {device_id} volume: {volume}')
    return True

# @timed_function
async def on_adjust_volume_callback(device_id: str, volume: int)->bool:
    print(f'device id: {device_id} volume: {volume}')
    return True

# @timed_function
async def on_media_control_callback(device_id: str, media_control: str)->bool:
    print(f'device id: {device_id} media control: {media_control}')
    return True

# @timed_function
async def on_select_input_callback(device_id: str, input: str)->bool:
    print(f'device id: {device_id} input: {input}')
    return True

# @timed_function
async def on_set_bands_callback(device_id: str, bands: str, level: int)->bool:
    print(f'device id: {device_id} bands: {bands}  level: {level}')
    return True

# @timed_function
async def on_set_mode_callback(device_id: str, mode: str)->bool:
    print(f'device id: {device_id} mode: {mode}')
    return True

# @timed_function
async def on_change_channel_callback(device_id: str, channel_name: str)->bool:
    print(f'device id: {device_id} channel name: {channel_name}')
    return True

# @timed_function
async def on_change_channel_number_callback(device_id: str, channel_name: str)->bool:
    print(f'device id: {device_id} channel name: {channel_name}')
    return True

# @timed_function
async def on_skip_channels_callback(device_id: str, channel_count: int)->bool:
    print(f'device id: {device_id} channel count: {channel_count}')
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
    global sinricpro_tv

    sinricpro.on_connected(on_connected)
    sinricpro.on_disconnected(on_disconnected)

    sinricpro_tv.on_power_state(on_power_state_callback)
    sinricpro_tv.on_mute(on_mute_callback)
    sinricpro_tv.on_set_volume(on_set_volume_callback)
    sinricpro_tv.on_adjust_volume(on_adjust_volume_callback)
    sinricpro_tv.on_media_control(on_media_control_callback)
    sinricpro_tv.on_select_input(on_select_input_callback)
    sinricpro_tv.on_set_bands(on_set_bands_callback)
    sinricpro_tv.on_set_mode(on_set_mode_callback)
    sinricpro_tv.on_change_channel(on_change_channel_callback)
    sinricpro_tv.on_change_channel_number(on_change_channel_number_callback)
    sinricpro_tv.on_skip_channels(on_skip_channels_callback)

    sinricpro.add_device(sinricpro_tv)
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