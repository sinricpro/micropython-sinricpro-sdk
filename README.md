# Micropython-SinricPro SDK

[![Discord](https://img.shields.io/badge/discord-%23micropython-blue.svg)](https://discord.gg/rq9vcRcSqA) </br>

The simple way to control your MicroPython board with Amazon Alexa, Google Home, SmartThings, Homebridge and Node-RED.

Tutorials: 

- ##### [How to turn on and off a Relay (ESP32)](https://help.sinric.pro/pages/tutorials/switch/micropython/how-to-turn-on-and-off-a-relay-using-micropython.html)

### Which device types are working as of now?

|Device Type |Supported ? | Example
|---        |---               |--- 
| `Switch`  | <ul><li>- [x] Completed</li></ul>           | [here](https://github.com/sinricpro/micropython-sinricpro-sdk/tree/main/examples/switch)
| `Blinds`  | <ul><li>- [x] Completed</li></ul> | [here](https://github.com/sinricpro/micropython-sinricpro-sdk/tree/main/examples/blinds)
| `Dimmable Switch` | <ul><li>- [x] Completed</li></ul>  | [here](https://github.com/sinricpro/micropython-sinricpro-sdk/tree/main/examples/dim-switch)
| `Fan` | <ul><li>- [x] Completed</li></ul> | [here](https://github.com/sinricpro/micropython-sinricpro-sdk/tree/main/examples/dim-switch)
| `Garage Door` | <ul><li>- [x] Completed</li></ul> | [here](https://github.com/sinricpro/micropython-sinricpro-sdk/tree/main/examples/fan)
| `Light` | <ul><li>- [x] Completed</li></ul>  | [here](https://github.com/sinricpro/micropython-sinricpro-sdk/tree/main/examples/light)
| `Lock` | <ul><li>- [x] Completed</li></ul> | [here](https://github.com/sinricpro/micropython-sinricpro-sdk/tree/main/examples/lock)
| `Thermostat` | <ul><li>- [x] Completed</li></ul>  | [here](https://github.com/sinricpro/micropython-sinricpro-sdk/tree/main/examples/thermostat)
| `TV` | <ul><li>- [x] Completed</li></ul> | [here](https://github.com/sinricpro/micropython-sinricpro-sdk/tree/main/examples/tv)
| `AC Unit` | <ul><li>- [x] Completed</li></ul> | [here](https://github.com/sinricpro/micropython-sinricpro-sdk/tree/main/examples/ac-unit)
| `Temperature Sensor` | <ul><li>- [x] Completed</li></ul> | [here](https://github.com/sinricpro/micropython-sinricpro-sdk/tree/main/examples/temperature_sensor)
| `Motion Sensor` | <ul><li>- [x] Completed</li></ul> | [here](https://github.com/sinricpro/micropython-sinricpro-sdk/tree/main/examples/motion-sensor) 
| `Contact Sensor` | <ul><li>- [x] Completed</li></ul> | [here](https://github.com/sinricpro/micropython-sinricpro-sdk/tree/main/examples/contact-sensor) 
| `Speaker` | <ul><li>- [x] Completed</li></ul> | [here](https://github.com/sinricpro/micropython-sinricpro-sdk/tree/main/examples/speaker) 
| `Custom Device Types` | Pending | - 

### How do I install it?

Using mpremote: (pip install --user mpremote)

**make sure device is not connected to IDE**

```
mpremote mip install github:sinricpro/micropython-sinricpro-sdk 
```

or

```
py -m mpremote connect <COM_PORT> mip install github:sinricpro/micropython-sinricpro-sdk
```

Using mip (in REPL):
```
import mip
mip.install("github:sinricpro/micropython-sinricpro-sdk")
```

SinrciPro library will be installed in the /lib folder. You can manually copy the `sinricpro` folder to /lib as well

## How can I use it?

Checkout the examples directory.


### Will it run on Microcontroller X?

Tested on

1. *MicroPython v1.27.0 on 2025-12-09 Generic ESP32 module with ESP32*

2. *MicroPython v1.27.0 on 2025-12-09; Raspberry Pi Pico W with RP2040*

### For development using PyMakr:

1. Install Micropython (https://docs.micropython.org/en/latest/esp32/tutorial/intro.html) 
2. Install PyMakr in VSCode
3. VSCode -> Open Workspace from File -> micropython-sinricpro-sdk.code-workspace
4. Create a new file called main.py to code.
5. Connect to ESP32 in PyMakr -> Upload -> Hardreset device.
6. Please use Pylint for formatting (https://marketplace.visualstudio.com/items?itemName=ms-python.pylint) 

Tutorial: [How to Control a Relay (Turn On/Off) Using MicroPython on an ESP32 with Pymakr](https://help.sinric.pro/pages/tutorials/switch/micropython/how-to-turn-on-and-off-a-relay-using-micropython)

### For development using Thonny:

1. Install Micropython (https://docs.micropython.org/en/latest/esp32/tutorial/intro.html](https://projects.raspberrypi.org/en/projects/get-started-pico-w/1)
2. Install SinricPro library

Tutorial: [How to Control a Relay (Turn On/Off) Using MicroPython on an Raspberry Pi Pico W with Thonny](https://help.sinric.pro/pages/tutorials/switch/micropython/how-to-turn-on-and-off-a-relay-using-micropython-raspberry-pi-picow-with-thonny)

### To remove the library manually:

```
import mip
mip.install("shutil")
import shutil
shutil.rmtree("/lib/sinricpro")
```

### To list files in ESP32 or PICOW
```
import os
def listdir(dir):
    for i in os.listdir(dir):
        print('{}/{}'.format(dir,i))
    
listdir("/")
```

## Join the community!
Join us on our [Official Discord Server](https://discord.gg/rq9vcRcSqA)!
