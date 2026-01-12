from machine import Pin, PWM
import utime


buzzer = PWM(Pin(13), freq=1000, duty_u16=0)

buzzer.duty_u16(32768)
i = 100
j = 750 

while True:
    buzzer.freq(i)
    buzzer.duty_u16(3000)
    i += 100
    print(i)
    utime.sleep(0.5)