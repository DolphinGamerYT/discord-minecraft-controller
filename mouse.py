from pynput.mouse import Button, Controller
import time
import asyncio

controller = Controller()
value = 0.5

async def leftclick(press):
    if press:
        controller.press(Button.left)
    else:
        controller.release(Button.left)

async def rightclick(press):
    if press:
        controller.press(Button.right)
    else:
        controller.release(Button.right)

async def move_smooth(xm, ym, t):
    for i in range(t):
        if i < t/2:
            h = i
        else:
            h = t - i
        controller.move(h*xm, h*ym)
        await asyncio.sleep(1/60)

async def move_left():
    await move_smooth(value*-1, 0, 40)

async def move_right():
    await move_smooth(value, 0, 40)

async def move_up():
    await move_smooth(0, value*-1, 40)

async def move_down():
    await move_smooth(0, value, 40)

async def do360():
    await move_smooth(11.15, 0, 40)

if __name__ == "__main__":
    print("Go to main.py to start the bot!\n")
    input("Press a key to close...")
