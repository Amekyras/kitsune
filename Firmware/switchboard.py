# pinouts and the like

#import utime
import micropython
import machine
from machine import Pin, PWM
from pinouts import board_pins
from neopixel import NeoPixel


import user_cfg

#buzzer_pin = 13
status_pin = 25
#control_led = 15
#control_pin = 14
pixel_pin = 23
#tx_pin = 0
#rx_pin = 1




pinout = board_pins #switch pinouts for ++ board are p10_pins

switch_pins = pinout["switch_pins"]
switch_ids = pinout["switch_ids"]

button_pins = pinout["button_pins"]
led_pins = pinout["led_pins"]
ids = pinout["ids"]

buzzer_pin = pinout["buzzer_pin"]
control_led = pinout["control_led"]
control_pin = pinout["control_pin"]




class runtime_config:
    """
    Runtime configuration for the firmware.

    Contains DIP switch values (must be read at startup), multibox settings, and buzzer settings.

    Read at runtime and not expected to be changed once play begins.
    """
    def __init__(self, switches, debug=False, test_speaker=False, autoreset=False, role="standalone", user_volume=user_cfg.volume, freqmod=user_cfg.freqmod, buzzer=None):


        self.debug = switches[0].value(pullup=1)
        self.mute = switches[1].value(pullup=1)
        self.test_speaker = switches[2].value(pullup=1)
        self.autoreset = switches[3].value(pullup=1)

        self.role = role
        self.volume = (user_volume * (user_cfg.max_volume_duty // 100)) # Convert percentage to duty cycle
        self.freqmod = freqmod  # Frequency modulation factor
        #self.chain_pos = 0  # Position in chain for multi-unit setups
        self.buzzer = PWM(Pin(buzzer_pin), freq=2500, duty_u16=0)
        self.buzzer_pin = Pin(buzzer_pin, Pin.OUT)
        self.status_led = Pin(status_pin, Pin.OUT)

        self.team_a_colour = user_cfg.team_a_colour
        self.team_b_colour = user_cfg.team_b_colour
        self.armed_colour = user_cfg.armed_colour
        self.def_colour = user_cfg.def_colour

        self.team_a_freq_offset = user_cfg.team_a_freq_offset
        self.team_b_freq_offset = user_cfg.team_b_freq_offset

        self.pixel = NeoPixel(Pin(pixel_pin), 1)
        self.pixel.fill((0, 0, 0))
        self.pixel.write()


        if self.mute:
            self.volume = 0

        print("Runtime Configuration:")
        print(f"  Debug Mode: {self.debug}")
        print(f"  Mute: {self.mute}")
        print(f"  Test Speaker: {self.test_speaker}")
        print(f"  Auto-reset: {self.autoreset}")
        print(f"  Role: {self.role}")
        print(f"  Volume (duty cycle): {self.volume}")
        print(f"  Frequency Modulation: {self.freqmod}")
        #print(f"  Chain Position: {self.chain_pos}")


