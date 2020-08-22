from pynput.mouse import Button, Controller
import time
import asyncio

mouse = Controller()

async def move_smooth(xm, ym, t):
    for i in range(t):
        if i < t/2:
            h = i
        else:
            h = t - i
        mouse.move(h*xm, h*ym)
        await asyncio.sleep(1/60)

async def move_left():
    await move_smooth(1, 0, 40)

async def move_right():
    await move_smooth(-1, 0, 40)

async def move_up():
    await move_smooth(0, 1, 40)

async def move_down():
    await move_smooth(0, -1, 40)
