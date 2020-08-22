import discord
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions, CommandNotFound
from discord.utils import get
import time
import asyncio
import datetime
import keyboard
import mouse
import yaml

with open('config.yml') as file:
    config = yaml.safe_load(file)

delay = 0.3
try:
    delay = float(config.get("keyword_delay"))
    print("Delay has been set as '{}'.\n".format(delay))
except:
    print("[Warning] Delay has been set to 0.3, since there's an invalid value on the config.\n")

bot = commands.Bot(command_prefix='s!')
bot.remove_command('help')

keys = {"w": keyboard.VK_W, "a": keyboard.VK_A, "s": keyboard.VK_S, "d": keyboard.VK_D, "space": keyboard.VK_SPACE, "sneak": keyboard.VK_SHIFT, "mleft": keyboard.VK_LEFTCLICK, "mright": keyboard.VK_RIGHTCLICK}

keyspressed = {"w": False, "a": False, "s": False, "d": False, "space": False, "sneak": False, "mleft": False, "mright": False}
numberCode = {1: keyboard.VK_1, 2: keyboard.VK_2, 3: keyboard.VK_3, 4: keyboard.VK_4, 5: keyboard.VK_5, 6: keyboard.VK_6, 7: keyboard.VK_7, 8: keyboard.VK_8, 9: keyboard.VK_9}

async def walk(key):
    if (keyspressed.get(key)):
        keyboard.ReleaseKey(keys[key])
        keyspressed[key] = False
    else:
        keyboard.PressKey(keys[key])
        keyspressed[key] = True

@bot.event
async def on_ready():
    print("Bot Started Correctly\n")
    print(f"Bot name: {bot.user.name}")
    print(f"Bot id: {bot.user.id}")


@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.channel.TextChannel):
        user = message.author
        msg = message.content.lower()
        params = msg.split(" ")

        for x in range(0, len(params)):
            used = false

            ## Keyboard

            # Movement

            if (params[x] == "w"):
                await walk("w")
            elif (params[x] == "a"):
                await walk("a")
            elif (params[x] == "s"):
                await walk("s")
            elif (params[x] == "d"):
                await walk("d")
            elif (params[x] == ("space") or params[x] == "saltar" or params[x] == "jump"):
                await walk("space")
            elif (params[x] == ("sneak") or params[x] == ("agachar") or params[x] == "shift"):
                await walk("space")

            elif (params[x] == "drop" or params[x] == "soltar" or params[x] == "q"):
                keyboard.ClickKey(keyboard.VK_Q)

            # Hotbar

            try:
                number = int(params[x])
                if (number >= 1 and number <= 9):
                    keyboard.ClickKey(numberCode[number])
            except:
                int

            ## Mouse

            if (params[x] == ("up") or params[x] == ("arriba")):
                await mouse.move_up()
            elif (params[x] == ("left") or params[x] == ("izquierda")):
                await mouse.move_left()
            elif (params[x] == ("down") or params[x] == ("abajo")):
                await mouse.move_down()
            elif (params[x] == ("right") or params[x] == ("derecha")):
                await mouse.move_right()
            elif (params[x] == "360"):
                await mouse.do360()

            elif (params[x] == ("pegar") or params[x] == ("punch") or params[x] == ("mine") or params[x] == ("minar") or params[x] == ("destruir") or params[x] == ("picar") or "izquierdo" in params[x]):
                key = "mleft"
                if (keyspressed.get(key)):
                    keyspressed[key] = False
                else:
                    keyspressed[key] = True
                await mouse.leftclick(keyspressed.get(key))
            elif (params[x] == ("colocar") or params[x] == ("block") or params[x] == ("bloquear") or params[x] == ("protect") or params[x] == ("proteger") or "derecho" in params[x]):
                key = "mright"
                if (keyspressed.get(key)):
                    keyspressed[key] = False
                else:
                    keyspressed[key] = True
                await mouse.rightclick(keyspressed.get(key))

            await asyncio.sleep(delay)


try:
    bot.run(config.get("bot_token"))
except:
    print("Token is invalid or not set!\n")
    input("Press a key to close...")
