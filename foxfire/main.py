import micropython
from machine import Pin, Timer
import utime
import random

micropython.alloc_emergency_exception_buf(256)

pins = [3, 7, 11, 15, 28, 27, 21, 17]

ctrl_pin = 29


class Pin_Tester():
    def __init__(self, pin)
        self.pin_id = pin
        self.pin = Pin(pin, Pin.OUT)
        self.timer = Timer(-1)