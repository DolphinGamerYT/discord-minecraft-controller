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

bot = commands.Bot(command_prefix='s!')
bot.remove_command('help')

TOKEN = 'NzQ2Njc4ODU3MjcyMjYyNzE2.X0D04A.Dp4vQI-cLKjVY5Qt7iG6XrqS7VI'
keys = {"w": keyboard.VK_W, "a": keyboard.VK_A, "s": keyboard.VK_S, "d": keyboard.VK_D, "mleft": keyboard.VK_LEFTCLICK, "mright": keyboard.VK_RIGHTCLICK}

keyspressed = {"w": False, "a": False, "s": False, "d": False, "mleft": False, "mright": False}

async def walk(key):
    if (keyspressed.get(key)):
        keyboard.ReleaseKey(keys[key])
        keyspressed[key] = False
        print(keyspressed)
    else:
        keyboard.PressKey(keys[key])
        keyspressed[key] = True
        print(keyspressed)

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

        # Keyboard

        if (msg.startswith("w")):
            walk("w")
        elif (msg.startswith("a")):
            walk("a")
        elif (msg.startswith("s")):
            walk("s")
        elif (msg.startswith("d")):
            walk("d")

        # Mouse

        if (msg.startswith("up") or msg.startswith("arriba")):
            mouse.move_up()
        elif (msg.startswith("left") or msg.startswith("izquierda")):
            mouse.move_left()
        elif (msg.startswith("down") or msg.startswith("abajo")):
            mouse.move_down()
        elif (msg.startswith("right") or msg.startswith("derecha")):
            mouse.move_right()

        elif (msg.startswith("pegar") or msg.startswith("punch") or msg.startswith("mine") or msg.startswith("minar") or msg.startswith("picar") or "izquierdo" in msg):
            key = "mleft"
            if (keyspressed.get(key)):
                keyboard.ReleaseKey(keys[key])
                keyspressed[key] = False
                print(keyspressed)
            else:
                keyboard.PressKey(keys[key])
                keyspressed[key] = True
                print(keyspressed)
        elif (msg.startswith("colocar") or msg.startswith("block") or msg.startswith("bloquear") or msg.startswith("protect") or msg.startswith("proteger") or "derecho" in msg):
            key = "mright"
            if (keyspressed.get(key)):
                keyboard.ReleaseKey(keys[key])
                keyspressed[key] = False
                print(keyspressed)
            else:
                keyboard.PressKey(keys[key])
                keyspressed[key] = True
                print(keyspressed)


bot.run(TOKEN)
