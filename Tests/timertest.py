import time
from machine import RTC, Timer
import random
import asyncio

increment = 0

a = 0
b = 0

def callbackinc(timer):
    global increment
    increment+=5

def compare (timer):
    pass

async def randomwork():
    work = 0
    for i in range(1,100):
        await asyncio.sleep(0)
        r = random.randint(1, 999999)
        work+=r

async def printer():
    await asyncio.sleep(1)
    a = increment
    print(a-1000)

tim = Timer()

tim.init(period=5, callback=callbackinc)



async def main():
    while True:
        await asyncio.gather(randomwork(), printer())

asyncio.run(main())