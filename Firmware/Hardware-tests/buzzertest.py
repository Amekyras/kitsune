import micropython
import utime
from machine import Pin, PWM

ledtest = Pin(18, Pin.OUT)

buzzertest = Pin (10, Pin.IN, Pin.PULL_DOWN)

while True:
    if buzzertest.value():
        ledtest.on()
        print("high")
    else:
        ledtest.off()
        print("low")