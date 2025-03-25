import utime
import micropython
from machine import *
from hardware import *
from functions import *
from classes import *
from neopixel import NeoPixel
from buzzer_music import music
import rp2


# make hardware class?






# starting variable values
#lock = True # lock prevents multiple buzzes
#flag = False # flag raised when buzz detected, signals loop to check active
#active = None # box that buzzed

config = runtime_config()

game = game_state()






def flash_pixel():
    r, g, b = pixel[0] # type: ignore
    if game.lock:
        if r == 0:
            pixel.fill((217, 121, 232))
        else:
            pixel.fill((0, 0, 0))

    #print(pixel, lock)
    pixel.write()
    pass
    #pixel_timer.init(mode=Timer.ONE_SHOT, period=1000, callback=flash_pixel(toggle))


def check_uart():
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
    # respond to raised flag
    status_timer.deinit()

    game.lock = True
    game.flag = False

    if mode == "main":
        uart.write("lock")

    control.led.off() # type: ignore
    game.active.led.on() # type: ignore
    pixel.fill((255, 0, 0))
    pixel.write()
    buzz(speaker=buzzer, config=config)

    if config.autoreset:
        reset_timer.init(mode=Timer.ONE_SHOT, period=10000, callback=autoresetter)


def reset_handler(mode):
    print("Resetting")
    reset_timer.deinit()

    for i in boxes:
        i.led.off()
    control.led.on() # type: ignore

    pixel.fill((0, 0, 0))
    pixel.write()

    if mode == 'main':
        uart.write("reset")
        #while True:
        #    if "ack" in check_uart():
        #        break

    if mode == 'branch':
        uart.write("ack\n")

    status_timer.init(period=1000, callback=status_toggle)
    game.lock = False


def autoresetter(t):
    reset_handler(role)

#setup hardware
buzzer = PWM(Pin(buzzer_pin), freq=2500, duty_u16=0)

status_led = Pin(status_pin, Pin.OUT)
status_led.off()
status_timer = Timer()

def status_toggle(t):
    status_led.toggle()

def prompt_toggle(t):
    control.led.toggle() # type: ignore


control = box(game, control_pin, led_pin=control_led, id="Control")
control.led.off() # type: ignore

boxes = []
for i in range(0, len(button_pins)):
    boxes.append(box(game, button_pin=button_pins[i], led_pin=led_pins[i], id=ids[i], irq=True))

for i in boxes:
    i.led.off()


### SWITCHBOARD ###
# 1 - DEBUG
# 2 - MUTE (must disable neopixel to read)
# 3 - EGG
# 4 - AUTORESET
# 5 - BRANCH
# 6 - ACTIVATE MULTIBUZZER
switches = []

for i in range(0, len(switch_pins)):
    switches.append(box(game, button_pin=switch_pins[i], id=switch_ids[i], pull="up"))

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
    reset_timer = Timer()

else: 
    config.autoreset = False
    

#initialise neopixel after mute check
pixel = NeoPixel(Pin(pixel_pin), 1)
pixel.fill((0, 0, 0))
pixel.write()


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



#startup sound
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

# check for multibuzzer
role = "standalone"
mb = False
if not switches[5].button.value():
    mb = True
    if not switches[4].button.value():
        role = "branch"
        print("Branch mode")
    else:
        role = "main"
        print("Main mode")
    uart = UART(0) 
    uart.init(tx=tx_pin, rx=rx_pin, bits=8, parity=None, stop=2, txbuf=32, rxbuf=32)
    uart.read()

else:
    print("Standalone mode")


print("Entering setup loop")

prompt_flash = Timer()
prompt_flash.init(period=1000, mode=Timer.PERIODIC, callback=prompt_toggle) # type: ignore

while True: 
    #setup check

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
        game.lock = False
        
        break
    elif role == 'branch':
        break


#main loop
prompt_flash.deinit()
status_timer.init(period=1000, callback=status_toggle)

print("Entering main loop")

    
game.lock = False

role = "standalone" # disable UART until further notice

if role == 'main':
    while True:
        if not game.lock:
            if "buzz" in check_uart():
                print("Buzz from branch")
                game.lock = True
                status_timer.deinit()
                uart.write("ack")
            
            if game.flag:
                bundle_handler(role)

        elif control.button.value() == 1:
            reset_handler(role)

elif role == 'branch':
    while True:

        if not game.lock:
            if game.flag:
                uart.write("buzz")
                while not game.lock:
                    if "ack" in check_uart():
                        bundle_handler(role)
                    elif "lock" in check_uart():
                        game.lock = True
                        status_timer.deinit()
            elif "lock" in check_uart():
                game.lock = True
                status_timer.deinit()

        elif "reset" in check_uart():
            print("Resetting branch")
            reset_handler(role)

else:
    
    while True:
        if not game.lock:
            control.led.on() # type: ignore
            if game.flag:
                bundle_handler(role)

        elif control.button.value() == 1:
            reset_handler(role)



        
     