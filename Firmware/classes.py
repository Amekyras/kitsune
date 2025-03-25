import micropython
import utime
from machine import *
#from functions import handle_buzz


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

config = runtime_config()    

game = game_state()



class box():
    """All inputs use this class, pass led_pin ID to add output"""
    def __init__(self, game_state, button_pin, handler=None, led_pin=None, id="", pull="down", irq=False):
        if pull == "up":
            self.button = Pin(button_pin, Pin.IN, Pin.PULL_UP)
        else:
            self.button = Pin(button_pin, Pin.IN, Pin.PULL_DOWN)

        if irq:
            self.button.irq(handler=self.handle_press)

        if led_pin is not None:
            self.led = Pin(led_pin, Pin.OUT)
        else:
            self.led = None
        
        self.id = id

        self.handler = handle_buzz
        
        self.lock = game_state.lock
        self.flag = game_state.flag
        self.active = game_state.active
        


    def handle_press(self, c):
        state = disable_irq()
        if not self.lock:
            micropython.schedule(self.handler, self)
            print(f"buzz from {self.id}")
        enable_irq(state)

    




def handle_buzz(arg):

    if not arg.flag:
        arg.lock = True
        arg.flag = True
        arg.active = arg

        print(f"Successful buzz from {arg.id}")

def buzz(speaker, config):
    #speaker.duty_u16(50000)
    volume = config.volume
    if not config.mute:
        speaker.duty_u16(62500)
        speaker.freq(900)

        speaker.freq(300)
        utime.sleep_ms(125)

        speaker.duty_u16(0)
        utime.sleep_ms(25)
        speaker.duty_u16(62500)

        speaker.freq(750)
        utime.sleep_ms(125)
        
        speaker.duty_u16(0)
        utime.sleep_ms(25)
        speaker.duty_u16(62500)
        
        speaker.freq(300)
        utime.sleep_ms(125)
        
        speaker.duty_u16(0)
        utime.sleep_ms(25)
        speaker.duty_u16(62500)

        speaker.freq(750)
        utime.sleep_ms(125)
        
        speaker.duty_u16(0)
        utime.sleep_ms(25)
        speaker.duty_u16(62500)

        speaker.freq(300)
        utime.sleep_ms(125)

        speaker.duty_u16(0)
    return()