# pinouts and the like

#import utime
#import micropython
#import machine
from user_cfg import *

buzzer_pin = 13
status_pin = 25
control_led = 15
control_pin = 14
pixel_pin = 23
#tx_pin = 0
#rx_pin = 1



p8_pins = {
    "switch_pins": [28, 23, 22, 12, 11, 10], #v0.2 pins
    "button_pins": [2, 4, 6, 8, 16, 18, 20, 26], #v0.2 pins
    "led_pins": [3, 5, 7, 9, 17, 19, 21, 27], #v0.2 pins
    "ids": ["A1", "A2", "A3", "A4", "B4", "B3", "B2", "B1"],
    "switch_ids": ["switch1", "switch2", "switch3", "switch4", "switch5", "switch6"],
}

p10_pins = {
    "switch_pins": [28, 23, 22, 12], 
    "button_pins": [2, 4, 6, 8, 0, 10, 16, 18, 20, 26], 
    "led_pins": [3, 5, 7, 9, 1, 11, 17, 19, 21, 27], 
    "ids": ["A1", "A2", "A3", "A4", "A5", "B5", "B4", "B3", "B2", "B1"],
    "switch_ids": ["switch1", "switch2", "switch3", "switch4"],
}

pinout = p10_pins #switch pinouts for ++ board are p10_pins

switch_pins = pinout["switch_pins"]
switch_ids = pinout["switch_ids"]

button_pins = pinout["button_pins"]
led_pins = pinout["led_pins"]
ids = pinout["ids"]




class runtime_config:
    def __init__(self, debug=False, test_speaker=False, autoreset=False, role="standalone", volume=100.0, freqmod=100.0):
        self.debug = debug
        self.test_speaker = test_speaker
        self.autoreset = autoreset
        self.role = role
        self.volume = round(volume * 65535 / 100)  # Convert percentage to duty cycle
        self.freqmod = freqmod  # Frequency modulation factor

        if self.volume > 0:
            self.mute = False
        else:
            self.mute = True

class game_state:
    def __init__(self, lock=False, flag=False, active=None):
        self.lock = lock
        self.flag = flag
        self.active = active
        self.debug = False

game = game_state()

config = runtime_config()