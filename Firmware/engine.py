#note: refining using Gemini https://gemini.google.com/app/39fc3339e3460a7a



import micropython
from machine import PWM, Pin, Timer, disable_irq, enable_irq
import utime
from lib.buzzer_music import music
from pinouts import board_pins


class player_box():
    """Non-controller boxes. Passes button presses to game engine."""
    def __init__(self, engine, button_obj, handler=None, led_obj=None, id="",  irq=False):

        self.button = button_obj
        self.engine = engine
        self.id = id

        if irq: #and not hardware_cfg.game.debug:
            self.button.irq(handler=self._handle_press, trigger=self.button.IRQ_RISING)


        if led_obj is not None:
            self.led = led_obj
        
        

    def update_led(self, state):
        if self.led is not None:
            if state:
                self.led.on()
            else:
                self.led.off()
        


    def _handle_press(self, _):
        state = disable_irq()
        micropython.schedule(self.engine.handle_buzz, self)
        enable_irq(state)






class kitsune_engine():



    def __init__(self, cfg, control_led):
        self.cfg = cfg
        self.locked = True
        self.active_player = None
        self.refractory = False
        self.ref_timer = Timer(-1)
        self.control_led = control_led
        self.team_offset = 1

    def handle_buzz(self, player):
        if self.locked or self.refractory: return
        
        self.locked = True
        self.control_led.off()
        self.active_player = player
        player.update_led(1)
        
        if "A" in player.id:
            self.cfg.pixel.fill(self.cfg.team_a_colour)
            self.team_offset = self.cfg.team_a_freq_offset
        elif "B" in player.id:
            self.cfg.pixel.fill(self.cfg.team_b_colour)
            self.team_offset = self.cfg.team_b_freq_offset
        else:
            self.cfg.pixel.fill(self.cfg.def_colour)
            self.team_offset = 1
        self.cfg.pixel.write()

        print(f"Buzzer locked by {player.id}")
        self.buzz(self.cfg)

    def reset(self):

        self.cfg.pixel.fill(self.cfg.armed_colour)
        self.cfg.pixel.write()
        self.control_led.on()

        self.refractory = True
        self.locked = False
        if self.active_player: self.active_player.update_led(0)
        self.active_player = None

        print ("Resetting")

        # Use timer to clear refractory period
        self.ref_timer.init(mode=Timer.ONE_SHOT, period=100, callback=self.reset_refractory)
        
    def reset_refractory(self, _):
        self.refractory = False
        print("cleared refractory period")
        


    def buzz(self, config=None):
        """
        Buzz the speaker with the given configuration.

        Args:
            config (runtime_config): The runtime configuration object.
        """
        if config is None:
            config = self.cfg
        speaker = PWM(config.buzzer_pin, freq=2500, duty_u16=0)
        #speaker.duty_u16(50000)
        volume = round(config.volume)
        freqmod = (config.freqmod/100) * self.team_offset
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
            speaker.deinit()
            print("End buzz")
        return()
    
    def buzz_startup(self):
        """
        Buzz the speaker with the given configuration.

        Args:
            config (runtime_config): The runtime configuration object.
        """
        volume = round(self.cfg.volume)
        print(f"Startup Buzzing at volume {volume}")

        jingletrack = "0 G5 1 15 0.5039370059967041;1 F#5 1 15 0.5039370059967041;3 E5 3 15 0.5039370059967041;6 F#5 2 15 0.5039370059967041"
        jingler = Pin(board_pins["buzzer_pin"])
        jingle = music(jingletrack, pin=jingler, looping=False, duty=volume)

        if not self.cfg.mute:
            print("Start startup buzz")
            while True:
                jingle.tick()
                utime.sleep(0.04)
                if jingle.stopped:
                    jingle.stop()
                    break
            print("End startup buzz")
        PWM(jingler).deinit()

        return()