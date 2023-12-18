from lib.sinricpro import SinricPro
from lib.sinricpro_switch import SinricProSwitch
import uasyncio as a 
import network

def on_power_state_callback(state):
    # Implement your logic to handle the power state change here
    return True, state

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    ap = network.WLAN(network.AP_IF) # create access-point interface
    ap.active(False)         # deactivate the interface
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.active(True)
        sta_if.connect("<wifiname>", "<wifipassword>")
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    a = sta_if.config('mac')
    print('MAC {:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(a[0],a[1],a[2],a[3],a[4]))

# main coroutine
async def main():
    do_connect()
    
    sinricpro = SinricPro()
    sinricpro_switch = SinricProSwitch("<deviceid>")
    sinricpro_switch.on_power_state(on_power_state_callback)
    
    sinricpro.add_device(sinricpro_switch)
    
    sinricpro.begin("<app_key>", "<app_secret>")

    while True:
        await a.sleep_ms(10_000)

# start asyncio task and loop
try:
    # start the main async tasks
    a.run(main())
finally:
    # reset and start a new event loop for the task scheduler
    a.new_event_loop()
