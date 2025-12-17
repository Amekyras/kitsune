import micropython
import utime
from machine import *
import hardware_cfg
import user_cfg
import mcp23017
#from functions import handle_buzz










class box():
    """All inputs use this class, pass led_pin ID to add output"""
    def __init__(self, game_state, button_pin, handler=None, led_pin=None, id="", pull="down", irq=False):
        #if mcp is not None:
        #    self.led_virtual = True
        #    self.mcp = mcp
        

        #if mcp_button is not None:
        #    self.button = mcp_button

        #if not mcp:
        #if pull == "up":
        #    self.button = Pin(button_pin, Pin.IN, Pin.PULL_UP)
        #else:
        #    self.button = Pin(button_pin, Pin.IN, Pin.PULL_DOWN)
        self.button = button_pin
        #print(type(self.button))
        if type(self.button) == "VirtualPin":
            self.button.input(pull=0 if pull=="down" else 1)
            #MCP DOES NOT HAVE PULLDOWN RESISTORS I THINK!!!
        #else:
        #    print("test")
        #    self.button = self.mcp[button_pin].input(pull=1)
        #    #self.button = mcp[button_pin]

        if irq and not hardware_cfg.game.debug:
            self.button.irq(handler=self.handle_press,trigger=Pin.IRQ_RISING)


        #if led_pin is not None and mcp is None:
        #    self.led = Pin(led_pin, Pin.OUT)
        #elif led_pin is not None and mcp is not None:
        #    self.led = mcp_led
        #    self.led
        if led_pin is not None:
            self.led = led_pin
            if type(self.led) == "VirtualPin":
                self.led.output() #type: ignore
        else:
            self.led = None
        
        self.id = id
        

        self.handler = handle_buzz
        
        #self.game = game_state
        #self.lock = game_state.lock
        #self.flag = game_state.flag
        #self.active = game_state.active
        


    def handle_press(self, c):
        state = disable_irq()
        if not hardware_cfg.game.lock:
            micropython.schedule(self.handler, self)
            print(f"buzz from {self.id}")
        else:
            print(f"locked-out buzz from {self.id}")
        enable_irq(state)



    def led_on(self):
        if self.led is not None:
            if type(self.led) == Pin:
                self.led.on()
            else:
                self.led.output(1) # type: ignore

    def led_off(self):
        if self.led is not None:
            if type(self.led) == Pin:
                self.led.off()
            else:
                self.led.output(0) # type: ignore


def handle_buzz(arg):
    """
    Handle a buzz event from a box.

    Args:
        arg (box): The box that triggered the buzz.
    """
    #hardware_cfg.game.lock = True
    hardware_cfg.game.flag = True
    hardware_cfg.game.active = arg

    #print(f"Successful buzz from {arg.id}")

def buzz(config):
    """
    Buzz the speaker with the given configuration.

    Args:
        config (runtime_config): The runtime configuration object.
    """
    speaker = config.buzzer
    #speaker.duty_u16(50000)
    volume = round(config.volume)
    freqmod = (config.freqmod/100)
    print(f"Buzzing at volume {volume} and freqmod {freqmod}")
    if not config.mute:
        print("Start buzz")
        speaker.duty_u16(volume)
        speaker.freq(round(900*freqmod))

        speaker.freq(round(300*freqmod))
        utime.sleep_ms(125)

        speaker.duty_u16(0)
        utime.sleep_ms(25)
        speaker.duty_u16(volume)

        speaker.freq(round(750*freqmod))
        utime.sleep_ms(125)
        
        speaker.duty_u16(0)
        utime.sleep_ms(25)
        speaker.duty_u16(volume)
        
        speaker.freq(round(300*freqmod))
        utime.sleep_ms(125)
        
        speaker.duty_u16(0)
        utime.sleep_ms(25)
        speaker.duty_u16(volume)

        speaker.freq(round(750*freqmod))
        utime.sleep_ms(125)
        
        speaker.duty_u16(0)
        utime.sleep_ms(25)
        speaker.duty_u16(volume)

        speaker.freq(round(300*freqmod))
        utime.sleep_ms(125)

        speaker.duty_u16(0)
        print("End buzz")
    return()




