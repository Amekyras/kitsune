from machine import Pin, I2C
from lib.mcp23017 import MCP23017
#import hardware_cfg as hw_cfg
from lib.shims import UnifiedPin

import pinouts
import user_cfg

pinout = pinouts.board_pins #switch pinouts for ++ board are p10_pins

switch_pins = pinout["switch_pins"]
switch_ids = pinout["switch_ids"]

button_pins = pinout["button_pins"]
led_pins = pinout["led_pins"]
ids = pinout["ids"]

buzzer_pin = pinout["buzzer_pin"]
control_led = pinout["control_led"]
control_pin = pinout["control_pin"]
has_mcp = pinout["mcp"]

def init_mcp():

    if not has_mcp:
        return None
    # Setup I2C and MCP
    i2c = I2C(0, scl=Pin(21), sda=Pin(20))
    mcp = MCP23017(i2c, 0x20)
    return mcp

def init_hardware():


    # Wrap Pins in Shims so they all work the same
    boxes = []
    if has_mcp:
        mcp = init_mcp()
    else:
        mcp = None

    for i in range(len(button_pins)):
        b = Pin(button_pins[i], Pin.IN, Pin.PULL_DOWN)

        if has_mcp:
            mcp.pin(led_pins[i], mode=0) # type: ignore
            l = UnifiedPin(mcp[led_pins[i]]) # type: ignore # MCP LED
        else:
            l = UnifiedPin(Pin(led_pins[i], Pin.OUT)) # GPIO LED

        boxes.append({'id': ids[i], 'btn': b, 'led': l})

    switches = []
    for i in range (len(switch_pins)):
        if has_mcp:
            mcp.pin(switch_pins[i], mode=1, pullup=True, polarity=1) # type: ignore
            s = UnifiedPin(mcp[switch_pins[i]]) # type: ignore # Virtual Switch
            switches.append(s)
        else:
            s = Pin(switch_pins[i], Pin.IN, Pin.PULL_UP)
            switches.append(s)
        
    return boxes, switches, mcp

def init_ctrl(mcp=None):
    ctrl_button = Pin(control_pin, Pin.IN, Pin.PULL_DOWN)
    if has_mcp:
        mcp.pin(control_led, mode=0) # type: ignore
        ctrl_led = UnifiedPin(mcp[control_led]) # type: ignore # MCP LED
    else:
        ctrl_led = Pin(control_led, Pin.OUT)
    return ctrl_button, ctrl_led