from machine import Pin, I2C
from Firmware.lib.mcp23017 import MCP23017
import hardware_cfg as hw_cfg
from shims import UnifiedPin

def init_hardware():
    # Setup I2C and MCP
    i2c = I2C(0, scl=Pin(21), sda=Pin(20))
    mcp = MCP23017(i2c, 0x20)
    
    # Wrap Pins in Shims so they all work the same
    players = []
    for i in range(len(hw_cfg.button_pins)):
        b = Pin(hw_cfg.button_pins[i], Pin.IN, Pin.PULL_UP)
        l = UnifiedPin(mcp[hw_cfg.led_pins[i]]) # Virtual LED
        players.append({'id': hw_cfg.ids[i], 'btn': b, 'led': l})
        
    return players, mcp