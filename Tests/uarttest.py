from machine import *
import rp2

uart = UART(0)



uart.init(parity=None, stop=2, tx=0, rx=1, txbuf=32, rxbuf=32)

while True:
    if uart.any():
        data = uart.read()
        print(data)