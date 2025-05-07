import utime
import micropython
from machine import *
import cfg
from functions import *
from classes import *
from neopixel import NeoPixel
from buzzer_music import music
import rp2

config = cfg.runtime_config()
#global buzz_timer

#region func defs

refractory = False

def reset_refractory(t):
    global refractory
    refractory = False
    
refractory_timer = Timer(-1)

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


def check_uart(uart):
    if uart.any():
        data = uart.read()
        if data:
            print(data)
            return str(data)
        else:
            return ""
    else:
        return ""

def bundle_handler(mode):
    print("Bundle called")
    # respond to raised flag
    status_timer.deinit()

    cfg.game.lock = True
    cfg.game.flag = False

    #if mode == "main":
    #    uart.write("lock")

    control.led.off() # type: ignore
    cfg.game.active.led.on() # type: ignore
    pixel.fill((255, 0, 0))
    pixel.write()
    #print(f"{cfg.game.active.id} at {buzz_timer}") # type: ignore
    buzz(speaker=buzzer, config=config)

    if config.autoreset:
        reset_timer.init(mode=Timer.ONE_SHOT, period=10000, callback=autoresetter)


def reset_handler(mode):
    print("Resetting")
    reset_timer.deinit()

    for i in boxes:
        i.led.off()
    #control.led.on() # type: ignore

    pixel.fill((0, 0, 0))
    pixel.write()

    #if mode == 'main':
    #    uart.write("reset")
    #    #while True:
        #    if "ack" in check_uart():
        #        break

    #if mode == 'branch':
    #    uart.write("ack\n")
    refractory_timer.init(period=200, mode=Timer.ONE_SHOT, callback=reset_refractory)
    status_timer.init(period=1000, callback=status_toggle)
    #utime.sleep_ms(200)
    buzz_timer = utime.ticks_ms() # reset timer
    cfg.game.lock = False


def autoresetter(t):
    reset_handler(role)




#endregion

#region setup hardware
buzzer = PWM(Pin(cfg.buzzer_pin), freq=2500, duty_u16=0)

status_led = Pin(cfg.status_pin, Pin.OUT)
status_led.off()
status_timer = Timer(-1)

#buzz_timer = utime.ticks_ms()

def status_toggle(t):
    status_led.toggle()
    #print(f" Locked: {cfg.game.lock}, Flag: {cfg.game.flag}, Active: {cfg.game.active}")

def prompt_toggle(t):
    control.led.toggle() # type: ignore

reset_timer = Timer(-1)


control = box(cfg.game, cfg.control_pin, led_pin=cfg.control_led, id="Control")
control.led.off() # type: ignore

boxes = []
for i in range(0, len(cfg.button_pins)):
    boxes.append(box(cfg.game, button_pin=cfg.button_pins[i], led_pin=cfg.led_pins[i], id=cfg.ids[i], irq=True))

for i in boxes:
    i.led.off()

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

for i in range(0, len(cfg.switch_pins)):
    switches.append(box(cfg.game, button_pin=cfg.switch_pins[i], id=cfg.switch_ids[i], pull="up"))

if not switches[0].button.value():
    config.debug = True

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
    
if not switches[4].button.value() and not switches[5].button.value():
    config.role = "branch"
elif switches[4].button.value() and not switches[5].button.value():
    config.role = "main"
else:
    config.role = "standalone"
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
    egg(song)
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

prompt_flash = Timer(-1)
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
        testboxes.extend(switches)
        testboxes.append(control)
        while True:
            low = []
            high = []
            for i in testboxes:
                if i.button.value() == 1:
                    high.append(i.id)
                    if i.led is not None:
                        i.led.on()
                else:
                    low.append(i.id)
                    if i.led is not None:
                        i.led.off()
            print(f"High = {high}, Low = {low}", end="\r")
            #print("cycle")

            
    
    elif control.button.value() == 1:
        cfg.game.lock = False
        
        break
    elif config.role == 'branch':
        break
#endregion

#region main loop
prompt_flash.deinit()
status_timer.init(period=1000, callback=status_toggle)

print("Entering main loop")

    
cfg.game.lock = False

role = "standalone" # disable UART until further notice
#buzz_timer = utime.ticks_ms() # reset timer



if False:#role == 'main':
    while True:
        if not cfg.game.lock:
            if "buzz" in check_uart():
                print("Buzz from branch")
                cfg.game.lock = True
                status_timer.deinit()
                uart.write("ack")
            
            if cfg.game.flag:
                bundle_handler(role)

        elif control.button.value() == 1:
            reset_handler(role)

elif False:# role == 'branch':
    while True:

        if not cfg.game.lock:
            if cfg.game.flag:
                uart.write("buzz")
                while not cfg.game.lock:
                    if "ack" in check_uart():
                        bundle_handler(role)
                    elif "lock" in check_uart():
                        cfg.game.lock = True
                        status_timer.deinit()
            elif "lock" in check_uart():
                cfg.game.lock = True
                status_timer.deinit()

        elif "reset" in check_uart():
            print("Resetting branch")
            reset_handler(role)

else:
    
    while True:
        if refractory:
            cfg.game.lock = False
            cfg.game.flag = False

        elif not cfg.game.lock:
            control.led.on() # type: ignore
            if cfg.game.flag:
                bundle_handler(role)

        elif control.button.value() == 1:
            reset_handler(role)

#endregion

        
     