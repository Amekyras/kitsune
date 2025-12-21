#note: refining using Gemini https://gemini.google.com/app/39fc3339e3460a7a



import micropython
from machine import Pin, Timer, disable_irq, enable_irq

class player_box():
    """Non-controller boxes. Passes button presses to game engine."""
    def __init__(self, engine, button_pin, handler=None, led_pin=None, id="",  irq=False):

        self.button = button_pin
        self.engine = engine
        #print(type(self.button))
        #if type(self.button) == "VirtualPin":
        #    self.button.input(pull=0 if pull=="down" else 1)
            #MCP DOES NOT HAVE PULLDOWN RESISTORS I THINK!!!
        #else:
        #    print("test")
        #    self.button = self.mcp[button_pin].input(pull=1)
        #    #self.button = mcp[button_pin]

        if irq: #and not hardware_cfg.game.debug:
            self.button.irq(handler=self._handle_press, trigger=self.button.IRQ_RISING)


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
        

        #self.handler = handle_buzz
        
        #self.game = game_state
        #self.lock = game_state.lock
        #self.flag = game_state.flag
        #self.active = game_state.active
        


    def _handle_press(self, _):
        state = disable_irq()
        micropython.schedule(self.engine.handle_buzz, self)
        enable_irq(state)



    def update_led(self, state):
            if self.led: self.led.value(state)


class kitsune_engine():
    def __init__(self, cfg):
        self.cfg = cfg
        self.locked = False
        self.active_player = None
        self.refractory = False
        self.ref_timer = Timer(-1)

    def handle_buzz(self, player):
        if self.locked or self.refractory: return
        
        self.locked = True
        self.active_player = player
        player.update_led(True)
        # Trigger your buzz sound logic here...
        print(f"Buzzer locked by {player.id}")

    def reset(self):
        self.refractory = True
        self.locked = False
        if self.active_player: self.active_player.update_led(False)
        self.active_player = None
        # Use timer to clear refractory period
        self.ref_timer.init(mode=Timer.ONE_SHOT, period=200, 
                            callback=lambda t: setattr(self, 'refractory', False))