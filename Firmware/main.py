import utime
import micropython
from machine import *
from neopixel import NeoPixel
from buzzer_music import music
import rp2

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

# starting variable values
lock = True
flag = False
active = None

def handle_buzz(box):
    #global lock
    global active
    global flag

    if not flag:
        #lock = True
        flag = True
        active = box

        print(f"Successful buzz from {box.id}")


class box:
    """All inputs use this class, pass led_pin ID to add output"""
    def __init__(self, button_pin, led_pin=None, id="", pull="down", irq=False):
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
        pass


    def handle_press(self, c):
        state = disable_irq()
        if not lock:
            micropython.schedule(handle_buzz, self)
            print(f"buzz from {self.id}")
        enable_irq(state)



def buzz(speaker):
    #speaker.duty_u16(50000)
    if not mute:
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


def flash_pixel():
    r, g, b = pixel[0] # type: ignore
    if lock:
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
    global lock
    global flag
    lock = True
    flag = False

    if mode == "main":
        uart.write("lock")

    control.led.off() # type: ignore
    active.led.on() # type: ignore
    pixel.fill((255, 0, 0))
    pixel.write()
    buzz(speaker=buzzer)

    if autoreset:
        reset_timer.init(mode=Timer.ONE_SHOT, period=10000, callback=autoresetter)


def reset_handler(mode):
    print("Resetting")
    reset_timer.deinit()
    global lock

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
    lock = False


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


control = box(control_pin, led_pin=control_led, id="Control")
control.led.off() # type: ignore

boxes = []
for i in range(0, len(button_pins)):
    boxes.append(box(button_pin=button_pins[i], led_pin=led_pins[i], id=ids[i], irq=True))

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
    switches.append(box(button_pin=switch_pins[i], id=switch_ids[i], pull="up"))

if not switches[1].button.value():
    mute = True
    print("Muted")
else: mute = False

if not switches[3].button.value():
    autoreset = True
    print("Autoreset enabled")
else: autoreset = False
reset_timer = Timer()

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


if not switches[2].button.value() and not mute:
    print("Testing speaker")
    egg(song)
### END EGG ###



#startup sound
jingletrack = "0 G5 1 15 0.5039370059967041;1 F#5 1 15 0.5039370059967041;3 E5 3 15 0.5039370059967041;6 F#5 2 15 0.5039370059967041"
jingle = music(jingletrack, pin=Pin(13), looping=False)
if not mute:
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
        lock = False
        
        break
    elif role == 'branch':
        break


#main loop
prompt_flash.deinit()
status_timer.init(period=1000, callback=status_toggle)

print("Entering main loop")

    
lock = False

role = "standalone" # disable UART until further notice

if role == 'main':
    while True:
        if not lock:
            if "buzz" in check_uart():
                print("Buzz from branch")
                lock = True
                status_timer.deinit()
                uart.write("ack")
            
            if flag:
                bundle_handler(role)

        elif control.button.value() == 1:
            reset_handler(role)

elif role == 'branch':
    while True:

        if not lock:
            if flag:
                uart.write("buzz")
                while not lock:
                    if "ack" in check_uart():
                        bundle_handler(role)
                    elif "lock" in check_uart():
                        lock = True
                        status_timer.deinit()
            elif "lock" in check_uart():
                lock = True
                status_timer.deinit()

        elif "reset" in check_uart():
            print("Resetting branch")
            reset_handler(role)

else:
    
    while True:
        if not lock:
            control.led.on() # type: ignore
            if flag:
                bundle_handler(role)

        elif control.button.value() == 1:
            reset_handler(role)



        
     