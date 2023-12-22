# Micropython-SinricPro SDK

Alexa, Google Home, SmartThings and cloud for MicroPython.

Still under development!

### Which device types are working as of now?

|Device Type |Supported ? | Notes
|---        |---               |--- 
| `Switch`  | <ul><li>- [x] Completed</li></ul>           | -
| `Blinds`  | <ul><li>- [x] Completed</li></ul> | -
| `Dimmable Switch` | <ul><li>- [x] Completed</li></ul>  | -
| `Fan` | <ul><li>- [x] Completed</li></ul> | -
| `Garage Door` | <ul><li>- [x] Completed</li></ul> | -
| `Light` | <ul><li>- [x] Completed</li></ul>  | -
| `Lock` | <ul><li>- [x] Completed</li></ul> | -
| `Thermostat` | <ul><li>- [x] Completed</li></ul>  | -
| `TV` | <ul><li>- [x] Completed</li></ul> | -
| `AC Unit` | <ul><li>- [x] Completed</li></ul> | -
| `Temperature Sensor` | <ul><li>- [x] Completed</li></ul> | -
| `Motion Sensor` | <ul><li>- [x] Completed</li></ul> | - 
| `Contact Sensor` | <ul><li>- [x] Completed</li></ul> | - 
| `Speaker` | <ul><li>- [x] Completed</li></ul> | - 
| `Custom Device Types` | - | - 

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

Using mip:
```
import mip
mip.install("github:sinricpro/micropython-sinricpro-sdk")
```

## How can I use it?

Checkout the examples directory.


### Will it run on Microcontroller X?

Code is being developed and tested on a ESP32 devkit with MicroPython 1.21

### For development using PyMakr:

1. Install Micropython (https://docs.micropython.org/en/latest/esp32/tutorial/intro.html) 
2. Install PyMakr in VSCode
3. VSCode -> Open Workspace from File -> micropython-sinricpro-sdk.code-workspace
4. Create a new file called main.py to code.
5. Connect to ESP32 in PyMakr -> Upload -> Hardreset device.
6. Please use Pylint for formatting (https://marketplace.visualstudio.com/items?itemName=ms-python.pylint) 
