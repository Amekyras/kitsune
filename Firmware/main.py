import cfg
from functions import *
from classes import * # type: ignore
from neopixel import NeoPixel
from buzzer_music import music
import rp2
import machine
from machine import Pin, I2C
import mcp23017

micropython.alloc_emergency_exception_buf(100)

config = cfg.runtime_config(volume=cfg.volume, freqmod=cfg.freqmod)
#global buzz_timer

#region vars
refractory_timer = Timer(-1) #prevents buzzes immediately after reset (200ms)
refractory = False

status_timer = Timer(-1) #flashes status LED every second
prompt_flash = Timer(-1) #flashes control LED to prompt start
reset_timer = Timer(-1) #resets buzzers after 10s


#endregion

#region func defs


def reset_refractory(t):
    global refractory
    refractory = False
     

def flash_pixel():
    r, g, b = pixel[0] # type: ignore
    if cfg.game.lock:
        if r == 0:
            pixel.fill((217, 121, 232))
        else:
            pixel.fill((0, 0, 0))

    #print(pixel, lock)
    pixel.write()
    pass
    #pixel_timer.init(mode=Timer.ONE_SHOT, period=1000, callback=flash_pixel(toggle))



def bundle_handler(mode):
    print("Bundle called")
    # respond to raised flag
    status_timer.deinit()

    cfg.game.lock = True
    cfg.game.flag = False

    control.led_off() # type: ignore
    cfg.game.active.led_on() # type: ignore

    if cfg.game.active.id[0] == "A": # type:ignore
        pixel.fill(cfg.teama_colour)
    elif cfg.game.active.id[0] == "B": # type:ignore
        pixel.fill(cfg.teamb_colour)
    else:
        pixel.fill(cfg.def_colour)
    pixel.write()
    buzz(speaker=buzzer, config=config)

    if config.autoreset:
        reset_timer.init(mode=Timer.ONE_SHOT, period=cfg.reset_duration, callback=autoresetter)


def reset_handler(mode):
    print("Resetting")
    reset_timer.deinit()

    print("Resetting boxes")

    for i in boxes:
        i.led_off()
    #control.led.on() # type: ignore

    print("Resetting pixel")

    pixel.fill((0, 0, 0))
    pixel.write()

    print("Resetting timers")

    refractory_timer.init(period=200, mode=Timer.ONE_SHOT, callback=reset_refractory)
    status_timer.init(period=1000, callback=status_toggle)

    print("Resetting game state")

    cfg.game.flag = False
    cfg.game.lock = False



def autoresetter(t):
    reset_handler(role)




#endregion

#region switchboard
### SWITCHBOARD ###
# 1 - DEBUG
# 2 - MUTE (must disable neopixel to read)
# 3 - EGG
# 4 - AUTORESET
# 5 - BRANCH
# 6 - ACTIVATE MULTIBUZZER
switches = []


if cfg.pinout == cfg.p10v1_pins:
    i2c = I2C(scl=Pin(21), sda=Pin(20))
    print(i2c.scan())
    mcp = mcp23017.MCP23017(i2c, 0x20)

    for i in range(0, len(cfg.switch_pins)):
        mcp.pin(cfg.switch_pins[i], mode=1, pullup=True)
        j = mcp[cfg.switch_pins[i]]
        #print(type(j))
        switches.append(box(cfg.game, button_pin=j, id=cfg.switch_ids[i], pull="up"))
else:
    for i in range(0, len(cfg.switch_pins)):
        j = Pin(cfg.switch_pins[i], Pin.IN, Pin.PULL_UP)
        switches.append(box(cfg.game, button_pin=j, id=cfg.switch_ids[i], pull="up"))

print (switches[0])
print (switches[0].button.value())
if not switches[0].button.value():
    print("Debug mode")
    config.debug = True
    cfg.game.debug = True

if not switches[1].button.value():
    config.volume = 0
    print("Muted")
else: 
    config.volume = 62500

if not switches[2].button.value():
    config.test_speaker = True

if not switches[3].button.value():
    config.autoreset = True
    print("Autoreset enabled")
else: 
    config.autoreset = False
    
#endregion

#region setup hardware
buzzer = PWM(Pin(cfg.buzzer_pin), freq=2500, duty_u16=0)

status_led = Pin(cfg.status_pin, Pin.OUT)
status_led.off()

#buzz_timer = utime.ticks_ms()

def status_toggle(t):
    status_led.toggle()
    #print(f" Locked: {cfg.game.lock}, Flag: {cfg.game.flag}, Active: {cfg.game.active}")


prompt = True
def prompt_toggle(t):
    global prompt
    #control.led.toggle() # type: ignore

    if not prompt:
        control.led_off() # type: ignore
        prompt = True
    else:
        control.led_on() # type: ignore
        prompt = False




boxes = []

if cfg.pinout == cfg.p10v1_pins:
    for i in range(0, len(cfg.led_pins)): # type: ignore
        mcp.pin(cfg.led_pins[i], mode=0)
        j = mcp[cfg.led_pins[i]]

        boxes.append(box(cfg.game, button_pin=Pin(cfg.button_pins[i]), led_pin=j, id=cfg.ids[i], irq=True))
    mcp.pin(cfg.control_led, mode=0)
    l = mcp[cfg.control_led]
    control = box(cfg.game, button_pin=Pin(cfg.control_pin), led_pin=l, id="Control")
    control.led_off() # type: ignore

else:
    for i in range(0, len(cfg.led_pins)): # type: ignore
        boxes.append(box(cfg.game, button_pin=Pin(cfg.button_pins[i]), led_pin=Pin(cfg.led_pins[i]), id=cfg.ids[i], irq=True))

    control = box(cfg.game, button_pin=Pin(cfg.control_pin), led_pin=Pin(cfg.control_led), id="Control")
    control.led.off() # type: ignore

for i in boxes:
    i.led_off()

#endregion





#initialise neopixel after mute check
pixel = NeoPixel(Pin(cfg.pixel_pin), 1)
pixel.fill((0, 0, 0))
pixel.write()

#region speaker test
### EASTER EGG DETECTION/EXECUTION ###
song = "cara.txt"
def egg(songfile):
    with open(songfile, "r", encoding="utf-8") as songf:
        song = songf.read()
    song.replace('\"', " ")
    song.replace('\'', " ")
    #print(song)
    track = music(song, pin = Pin(13))
    while True:
        track.tick()
        utime.sleep(0.04)


if config.test_speaker and not config.mute:
    print("Testing speaker")
    #egg(song)
### END EGG ###
#endregion

#region startup sound
jingletrack = "0 G5 1 15 0.5039370059967041;1 F#5 1 15 0.5039370059967041;3 E5 3 15 0.5039370059967041;6 F#5 2 15 0.5039370059967041"
jingle = music(jingletrack, pin=Pin(13), looping=False)
if not config.mute:
    while True:
        jingle.tick()
        utime.sleep(0.04)
        if jingle.stopped:
            buzzer.duty_u16(0)
            break
buzzer.duty_u16(0) #kill buzzer

#endregion

#region setup loop
print("Entering setup loop")

prompt_flash.init(period=1000, mode=Timer.PERIODIC, callback=prompt_toggle) # type: ignore

while True: #setup check
    

    if not switches[0].button.value():
        prompt_flash.deinit()
        print("Debugging")
        pixel.fill((0, 255, 0))
        pixel.write()
        
        #buzzer test loop
        testboxes = []
        testboxes.extend(boxes)
        for i in testboxes:
            i.button.irq(handler=None)
        testboxes.extend(switches)
        testboxes.append(control)
        while True:
            low = []
            high = []
            for i in testboxes:
                if i.button.value() == 1:
                    high.append(i.id)
                    if i.led is not None:
                        i.led_on()
                else:
                    low.append(i.id)
                    if i.led is not None:
                        i.led_off()
            print(f"High = {high}, Low = {low}", end="\r")
            #print("cycle")

            
    
    elif control.button.value() == 1:
        cfg.game.lock = False
        print("Launching")
        break
    

    else:
        for i in boxes:
            i.led_on()
        
    #elif config.role == 'branch':
    #    break
#endregion

#region main loop
prompt_flash.deinit()
status_timer.init(period=1000, callback=status_toggle)

print("Entering main loop")

#cfg.game.flag = False
#cfg.game.lock = False

#for i in boxes:
#            i.led.off()

role = "standalone" # disable UART until further notice
reset_handler(role)
cfg.game.lock = False
cfg.game.flag = False

try:
    while True:
        if refractory and (cfg.game.lock or cfg.game.flag):
            cfg.game.lock = False
            cfg.game.flag = False

        elif not cfg.game.lock:
            control.led_on() # type: ignore
            if cfg.game.flag:
                bundle_handler(role)

        elif control.button.value() == 1: #query control box rather than resetting on interrupt
            reset_handler(role)
except Exception as e:
    print("Fatal error, resetting")

machine.reset()

#endregion

        
     