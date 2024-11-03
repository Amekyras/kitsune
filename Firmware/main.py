import micropython
import utime
from machine import Pin, PWM
#import asyncio

# button pins

class box:
    def __init__(self, button_pin, led_pin):
        self.button = Pin(button_pin, Pin.IN, Pin.PULL_DOWN)
        self.led = Pin(led_pin, Pin.OUT)
        pass


buzzer = PWM(Pin(13), freq=2500, duty_u16=0)


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





status_led = Pin("gpio25", Pin.OUT)
control = box(14, 15)

button_pins = [2, 4, 6, 8, 16, 18, 20, 26]
led_pins = [3, 5, 7, 9, 17, 19, 21, 27]

boxes = []

for i in range(0, len(button_pins)):
    boxes.append(box(button_pin=button_pins[i], led_pin=led_pins[i]))

lock = False
pulse = 0

while True:
    if not lock:
        control.led.on()
        for i in boxes:
            if i.button.value() == 1:
                lock = True
                i.led.on()
                control.led.off()
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
            control.led.on()

        
    