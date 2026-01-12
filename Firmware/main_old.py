import Firmware.switchboard as switchboard
import user_cfg
from classes import * # type: ignore
from neopixel import NeoPixel
from lib.buzzer_music import music
import rp2
import micropython
import machine
from machine import Pin, I2C, UART, PWM
import lib.mcp23017 as mcp23017
import os
import utime


micropython.alloc_emergency_exception_buf(100)

print(os.uname())
print(f"Firmware version: {switchboard.firmware_version}")
print(f"Pinout: {switchboard.pinout["name"]}")

cfg = switchboard.runtime_config()
# cfg is the global configuration object. this is an anti-pattern but it's late and I'm tired.

#hardware_cfg.game = hardware_cfg.game_state()



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
    if switchboard.game.lock:
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
    #status_timer.deinit()

    switchboard.game.lock = True
    switchboard.game.flag = False

    control.led_off() # type: ignore
    switchboard.game.active.led_on() # type: ignore

    if switchboard.game.active.id[0] == "A": # type:ignore
        pixel.fill(user_cfg.teama_colour)
    elif switchboard.game.active.id[0] == "B": # type:ignore
        pixel.fill(user_cfg.teamb_colour)
    else:
        pixel.fill(user_cfg.def_colour)
    pixel.write()
    try:
        print(cfg.volume)
        micropython.schedule(buzz, cfg)
    except Exception as e:
        print(f"Error during buzz: {e}")
    cfg.buzzer.duty_u16(0)
    if cfg.autoreset:
        reset_timer.init(mode=Timer.ONE_SHOT, period=user_cfg.reset_duration, callback=autoresetter)


def reset_handler(mode):
    print("Resetting")
    reset_timer.deinit()

    print("Resetting boxes")

    for i in boxes:
        i.led_off()
    #control.led.on() # type: ignore

    print("Resetting pixel")

    pixel.fill(user_cfg.armed_colour)
    pixel.write()

    print("Resetting timers")

    refractory_timer.init(period=200, mode=Timer.ONE_SHOT, callback=reset_refractory)
    #status_timer.init(period=1000, callback=status_toggle)

    print("Resetting game state")

    switchboard.game.flag = False
    switchboard.game.lock = False



def autoresetter(t):
    reset_handler(role)

def upstream_receive(t):
    micropython.schedule(chain_handle, t)

def downstream_receive(t):
    micropython.schedule(chain_handle, t)

def chain_handle(t):
    if t == upstream:
        if upstream.any():
            data = upstream.read()
            print(f"Upstream data: {data}")
            if "ACK" in data.decode('utf-8') and switchboard.game.active is not None:
                print("ACK received from upstream")
                bundle_handler("chain")
            elif "ACK" in data.decode('utf-8') and switchboard.game.active is None:
                print("ACK received from upstream with no active box")
                downstream.write("ACK")
            if "RESET" in data.decode('utf-8'):
                downstream.write("RESET")
                reset_handler("chain")
            
    elif t == downstream:
        if downstream.any():
            data = downstream.read()
            print(f"Downstream data: {data}")
            if "FLAG" in data.decode('utf-8'):
                switchboard.game.lock = True
                print("Flag received from downstream")
                downstream.write(f"ACK {data[4]}")

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


if switchboard.pinout["name"] == "v1.0++":
    i2c = I2C(scl=Pin(21), sda=Pin(20))
    print(i2c.scan())
    mcp = mcp23017.MCP23017(i2c, 0x20)

    for i in range(0, len(switchboard.switch_pins)):
        mcp.pin(switchboard.switch_pins[i], mode=1, pullup=True)
        j = mcp[switchboard.switch_pins[i]]
        #print(type(j))
        switches.append(box(switchboard.game, button_pin=j, id=switchboard.switch_ids[i], pull="up"))
else:
    for i in range(0, len(switchboard.switch_pins)):
        j = Pin(switchboard.switch_pins[i], Pin.IN, Pin.PULL_UP)
        switches.append(box(switchboard.game, button_pin=j, id=switchboard.switch_ids[i], pull="up"))

print (switches[0])
print (switches[0].button.value())
if not switches[0].button.value():
    print("Debug mode")
    #cfg.debug = True
    switchboard.game.debug = True

if not switches[1].button.value():
    cfg.volume = 0
    print("Muted")

if not switches[2].button.value():
    cfg.test_speaker = True

if not switches[3].button.value():
    cfg.autoreset = True
    print("Autoreset enabled")
else: 
    cfg.autoreset = False

#endregion

#region setup hardware

status_led = Pin(switchboard.status_pin, Pin.OUT)
status_led.off()

#buzz_timer = utime.ticks_ms()

last_msg = ""

def status_toggle(t):
    status_led.toggle()
    global last_msg
    msg = f" Lock: {switchboard.game.lock}, Flag: {switchboard.game.flag}, Active: {switchboard.game.active}"
    if msg != last_msg:
        last_msg = msg
        print(msg)


prompt = True
def prompt_toggle(t):
    global prompt
    #TODO: there's a bug here that makes the LED stay on sometimes
    #control.led.toggle() # type: ignore
    if not prompt:
        control.led_off() # type: ignore
        prompt = True
    else:
        control.led_on() # type: ignore
        prompt = False




boxes = []

if switchboard.pinout == switchboard.p10v1_pins:
    for i in range(0, len(switchboard.led_pins)): # type: ignore
        mcp.pin(switchboard.led_pins[i], mode=0)
        j = mcp[switchboard.led_pins[i]]

        boxes.append(box(switchboard.game, button_pin=Pin(switchboard.button_pins[i]), led_pin=j, id=switchboard.ids[i], irq=True))
    mcp.pin(switchboard.control_led, mode=0)
    l = mcp[switchboard.control_led]
    control = box(switchboard.game, button_pin=Pin(switchboard.control_pin), led_pin=l, id="Control")
    control.led_off() # type: ignore

else:
    for i in range(0, len(switchboard.led_pins)): # type: ignore
        boxes.append(box(switchboard.game, button_pin=Pin(switchboard.button_pins[i]), led_pin=Pin(switchboard.led_pins[i]), id=switchboard.ids[i], irq=True))

    control = box(switchboard.game, button_pin=Pin(switchboard.control_pin), led_pin=Pin(switchboard.control_led), id="Control")
    control.led.off() # type: ignore

for i in boxes:
    i.led_off()

#endregion

#region uart setup
if switchboard.pinout["name"] == "v1.0++":
    downstream = UART(0)
    upstream = UART(1)

    upstream.init(parity=None, stop=2, tx=4, rx=5, txbuf=32, rxbuf=32)
    downstream.init(parity=None, stop=2, tx=0, rx=1, txbuf=32, rxbuf=32)



#endregion



#initialise neopixel after mute check
pixel = NeoPixel(Pin(switchboard.pixel_pin), 1)
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


if cfg.test_speaker and not cfg.mute:
    print("Testing speaker")
    #egg(song)
### END EGG ###
#endregion

#region startup sound
jingletrack = "0 G5 1 15 0.5039370059967041;1 F#5 1 15 0.5039370059967041;3 E5 3 15 0.5039370059967041;6 F#5 2 15 0.5039370059967041"
jingle = music(jingletrack, pin=Pin(13), looping=False)
if not cfg.mute:
    while True:
        jingle.tick()
        utime.sleep(0.04)
        if jingle.stopped:
            cfg.buzzer.duty_u16(0)
            break
cfg.buzzer.duty_u16(0) #kill buzzer

#endregion

#region setup loop
print("Entering setup loop")

prompt_flash.init(period=1000, mode=Timer.PERIODIC, callback=prompt_toggle) # type: ignore

has_upstream = False
has_downstream = False 
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

    # do uart startup
    if switchboard.pinout["name"] == "v1.0++":
        #while True:

        upstream.write("Hello from downstream!")
        downstream.write("Hello from upstream!")
        utime.sleep(0.1)
    
        if upstream.any():
            has_upstream = True
            upstream_data = upstream.read()
            print(f"Upstream data: {upstream_data}")
            # control box no longer does anything
            # setup interrupts
            prompt_flash.deinit()
            status_led.on()
            print("Connected to upstream")
            upstream.irq(handler=upstream_receive, trigger=UART.RX_IDLE)

        if downstream.any():
            has_downstream = True
            downstream_data = downstream.read()
            print(f"Downstream data: {downstream_data}")
            downstream.irq(handler=downstream_receive, trigger=UART.RX_IDLE)
            # setup interrupts
            
    
    if not has_upstream and control.button.value() == 1:
        

        switchboard.game.lock = False
        print("Launching")
        break
    

    for i in boxes:
        i.led_on()
        
    #elif config.role == 'branch':
    #    break
#endregion

#region main loop
prompt_flash.deinit()
status_timer.init(period=1000, callback=status_toggle)

print("Entering main loop")

if not has_upstream and not has_downstream:
    role = "standalone" # disable UART until further notice
elif has_downstream and not has_upstream:
    role = "head"
else:
    role = "chain"
reset_handler(role)
switchboard.game.lock = False
switchboard.game.flag = False

role = "standalone" # TEMP OVERRIDE FOR TESTING WITHOUT UART

if role == "standalone":
    #upstream.deinit()
    #downstream.deinit()
    try:
        while True:
            try:
                if refractory and (switchboard.game.lock or switchboard.game.flag):
                    switchboard.game.lock = False
                    switchboard.game.flag = False

                elif not switchboard.game.lock:
                    control.led_on() # type: ignore
                    if switchboard.game.flag:
                        bundle_handler(role)

                elif control.button.value() == 1: #query control box rather than resetting on interrupt
                    reset_handler(role)
            except Exception as e:
                print(f"Error in main loop: {e}")
                pass
    except Exception as e:
        print("Fatal error, resetting")


elif role == "head":
    downstream.write("RESET")
    while True:
        if refractory and (switchboard.game.lock or switchboard.game.flag):
            switchboard.game.lock = False
            switchboard.game.flag = False

        elif not switchboard.game.lock:
            if downstream.any():
                data = downstream.read()
                if "FLAG" in data.decode('utf-8'):
                    switchboard.game.flag = True
                    switchboard.game.lock = True
                    print("Flag received from downstream")
                    downstream.write(f"ACK {data[4]}")

            control.led_on() # type: ignore
            if switchboard.game.flag:
                bundle_handler(role)


        elif control.button.value() == 1:
            #query control box rather than resetting on interrupt
            reset_handler(role)

else:
    pass

machine.reset()

#endregion

        
     