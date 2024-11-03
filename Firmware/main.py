import micropython
import utime
from machine import Pin, PWM
import asyncio

# button pins

class box:
    def __init__(self, button_pin, led_pin):
        self.button = Pin(button_pin, Pin.IN, Pin.PULL_DOWN)
        self.led = Pin(led_pin, Pin.OUT)
        pass


async def flash(pin, period, decay=0):
    cycles = 0
    #Pin object connected to LED

    while True:
        if period == 0:
            break

        pin.toggle()
        print(f"Flashing {pin}")
        await asyncio.sleep(period)

        if decay != 0:
            cycles +=1
            if decay >= cycles:
                break
    return()


buzzer = PWM(Pin(13), freq=2500, duty_u16=0)


async def buzz(speaker):
    #speaker.duty_u16(50000)

    speaker.duty_u16(50000)
    speaker.freq(900)

    speaker.freq(300)
    await asyncio.sleep(0.125)

    speaker.duty_u16(0)
    await asyncio.sleep(0.25)
    speaker.duty_u16(50000)

    speaker.freq(750)
    await asyncio.sleep(0.125)
    
    speaker.duty_u16(0)
    await asyncio.sleep(0.25)
    speaker.duty_u16(50000)
    
    speaker.freq(300)
    await asyncio.sleep(0.125)
    
    speaker.duty_u16(0)
    await asyncio.sleep(0.25)
    speaker.duty_u16(50000)

    speaker.freq(750)
    await asyncio.sleep(0.125)
    
    speaker.duty_u16(0)
    await asyncio.sleep(0.25)
    speaker.duty_u16(50000)

    speaker.freq(300)
    await asyncio.sleep(0.125)

    speaker.duty_u16(0)
    return()





status_led = Pin(25, Pin.OUT)
control = box(14, 15)

button_pins = [2, 4, 6, 8, 16, 18, 20, 26]
led_pins = [3, 5, 7, 9, 17, 19, 21, 27]

boxes = []

for i in range(0, len(button_pins)):
    boxes.append(box(button_pin=button_pins[i], led_pin=led_pins[i]))

lock = False
#pulse = 0


async def main():

    #wait for control box press to trigger
    lock = True
    control.led.off()
    while True:
        if control.button.value() == 1:
            control.led.on()
            flashtask = asyncio.create_task(flash(status_led, period=1))
            lock = False
            break

    while True:
        await asyncio.sleep(0)
        if not lock:
            #control.led.on()

            for i in boxes:
                if i.button.value() == 1:
                    lock = True
                    i.led.on()
                    control.led.off()
                    asyncio.run(buzz(speaker=buzzer))
                    flashtask.cancel()
                    break

        

        else:
            if control.button.value() == 1:
                print("Resetting")
                lock = False
                pulse = 0
                
                for i in boxes:
                    i.led.off()
                control.led.on()
                flashtask = asyncio.create_task(flash(status_led, 1))

asyncio.run(main())      
    