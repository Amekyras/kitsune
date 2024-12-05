#import micropython
import utime
from machine import Pin, PWM, Timer
from neopixel import NeoPixel
#import asyncio
from buzzer_music import music
# button pins
import json

class box:
    def __init__(self, button_pin, led_pin=None, id="", pull="down"):
        if pull == "up":
            self.button = Pin(button_pin, Pin.IN, Pin.PULL_UP)
        else:
            self.button = Pin(button_pin, Pin.IN, Pin.PULL_DOWN)

        if led_pin != None:
            self.led = Pin(led_pin, Pin.OUT)
        else:
            self.led = None
        self.id = id
        pass


    def handle_buzz(c):

        pass



buzzer = PWM(Pin(13), freq=2500, duty_u16=0)

pixel_pin = Pin(23, Pin.OUT)

pixel = NeoPixel(pixel_pin, 1)
pixel.fill((0, 0, 0))
pixel.write()

def buzz(speaker):
    #speaker.duty_u16(50000)

    speaker.duty_u16(50000)
    speaker.freq(900)

    speaker.freq(300)
    utime.sleep_ms(125)

    speaker.duty_u16(0)
    utime.sleep_ms(25)
    speaker.duty_u16(50000)

    speaker.freq(750)
    utime.sleep_ms(125)
    
    speaker.duty_u16(0)
    utime.sleep_ms(25)
    speaker.duty_u16(50000)
    
    speaker.freq(300)
    utime.sleep_ms(125)
    
    speaker.duty_u16(0)
    utime.sleep_ms(25)
    speaker.duty_u16(50000)

    speaker.freq(750)
    utime.sleep_ms(125)
    
    speaker.duty_u16(0)
    utime.sleep_ms(25)
    speaker.duty_u16(50000)

    speaker.freq(300)
    utime.sleep_ms(125)

    speaker.duty_u16(0)
    return()



pixel_timer = Timer()


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

    
song = "cara.txt"


def egg(songfile):
    with open(songfile, "r", encoding="utf-8") as songf:
        song = songf.read()
    song.replace('\"', " ")
    song.replace('\'', " ")
    print(song)
    track = music(song, pin = Pin(13))
    while True:
        track.tick()
        utime.sleep(0.04)


egghigh = Pin(10, Pin.OUT, value=1)
eggpin = Pin(11, Pin.IN, Pin.PULL_DOWN)

if eggpin.value():
    egg(song)

egghigh.init()

#egg
jumps= []
jumps.append(box(button_pin=12, id="jump1", pull="up"))
jumps.append(box(button_pin=11, id="jump2", pull="up"))
jumps.append(box(button_pin=10, id="jump3", pull="up"))


status_led = Pin(25, Pin.OUT)
control = box(14, led_pin=15, id="Control")




button_pins = [2, 4, 6, 8, 16, 18, 20, 26]
led_pins = [3, 5, 7, 9, 17, 19, 21, 27]
ids = ["A1", "A2", "A3", "A4", "B4", "B3", "B2", "B1"]

boxes = []

for i in range(0, len(button_pins)):
    boxes.append(box(button_pin=button_pins[i], led_pin=led_pins[i], id=ids[i]))

lock = True
pulse = 0

status_led.off()
control.led.off() # type: ignore



print("Entering setup loop")

jingletrack = "0 G5 1 15 0.5039370059967041;1 F#5 1 15 0.5039370059967041;3 E5 3 15 0.5039370059967041;6 F#5 2 15 0.5039370059967041"

jingle = music(jingletrack, pin=Pin(13), looping=False)

while True:
    jingle.tick()
    utime.sleep(0.04)
    if jingle.stopped:
        break

while True:
    #setup check

    if not jumps[0].button.value():
        
        #buzzer test loop
        testboxes = []
        testboxes.extend(boxes)
        testboxes.extend(jumps)
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

#main loop
print("Entering main loop")

while True:
    if not lock:
        control.led.on() # type: ignore
        for i in boxes:
            if i.button.value() == 1:
                lock = True
                i.led.on()
                control.led.off() # type: ignore
                pixel.fill((255, 0, 0))
                pixel.write()
                buzz(speaker=buzzer)
                break
        pulse +=1
        #gc.collect()
        if pulse % 10000 == 0:
            for x in boxes:
                print(x.button.value())
            status_led.toggle()
            print (pulse)

    else:
        if control.button.value() == 1:
            print("Resetting")
            lock = False
            pulse = 0
            
            for i in boxes:
                i.led.off()
            control.led.on() # type: ignore
            pixel.fill((0, 0, 0))
            pixel.write()




        
    