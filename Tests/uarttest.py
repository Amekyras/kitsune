from machine import *
import rp2
import utime

downstream = UART(0)
upstream = UART(1)


downstream.init(parity=None, stop=2, tx=4, rx=5, txbuf=32, rxbuf=32)
upstream.init(parity=None, stop=2, tx=0, rx=1, txbuf=32, rxbuf=32)

while True:
    if upstream.any():
        upstream_data = upstream.read()
        print(f"Upstream data: {upstream_data}")
        upstream.write(b"Hello from downstream!\n")
    else:
        downstream_data = downstream.read()
        print(f"Downstream data: {downstream_data}")
        downstream.write(b'Hello from upstream!\n')
    utime.sleep(1000)