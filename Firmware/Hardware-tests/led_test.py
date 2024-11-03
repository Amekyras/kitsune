import micropython
import utime
from machine import Pin, PWM#


pins = []
for i in range (0,28):
    pins.append(Pin(i, Pin.OUT))

while True:
    for i in pins:
        i.on()
        print(i)
        utime.sleep(1)
        i.off()
