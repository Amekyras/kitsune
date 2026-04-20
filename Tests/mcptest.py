from machine import Pin, I2C
import mcp23017
i2c = I2C( scl=Pin(21), sda=Pin(20))
#while True:
#    print(i2c.scan())
mcp = mcp23017.MCP23017(i2c, 0x20)

mcp.pin(10, mode=0, value=1)