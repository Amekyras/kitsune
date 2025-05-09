import utime
import micropython
from machine import *

buzzer_pin = 13
status_pin = 25
control_led = 15
control_pin = 14
pixel_pin = 23
tx_pin = 0
rx_pin = 1

switch_pins = [28, 23, 22, 12, 11, 10] #v0.2 pins
switch_ids = ["switch1", "switch2", "switch3", "switch4", "switch5", "switch6"]

button_pins = [2, 4, 6, 8, 16, 18, 20, 26] #v0.2 pins
led_pins = [3, 5, 7, 9, 17, 19, 21, 27] #v0.2 pins
ids = ["A1", "A2", "A3", "A4", "B4", "B3", "B2", "B1"]


class runtime_config:
    def __init__(self, debug=False, test_speaker=False, autoreset=False, role="standalone", volume=62500):
        self.debug = debug
        self.test_speaker = test_speaker
        self.autoreset = autoreset
        self.role = role
        self.volume = volume

        if self.volume > 0:
            self.mute = False
        else:
            self.mute = True

class game_state:
    def __init__(self, lock=False, flag=False, active=None):
        self.lock = lock
        self.flag = flag
        self.active = active

game = game_state()