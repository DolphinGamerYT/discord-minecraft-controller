import discord
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions, CommandNotFound
from discord.utils import get
import asyncio
from modules import keyboard, mouse
import yaml
import os

config = {}

if (os.path.isfile("./config.yml")):
    with open('config.yml') as file:
        config = yaml.safe_load(file)
else:
    f = open("config.yml","w")
    f.write("#####################################\n")
    f.write("##                                 ##\n")
    f.write("##    Minecraft Discord Edition    ##\n")
    f.write("##          By Dolphln             ##\n")
    f.write("##                                 ##\n")
    f.write("#####################################\n")
    f.write("\n")
    f.write("bot_token: 'your-bot-token-here'\n")
    f.write("keyword_delay: 0.3\n")
    f.close()
    file = open("config.yml")
    config = yaml.safe_load(file)

delay = 0.3
try:
    delay = float(config.get("keyword_delay"))
    print("Delay has been set as '{}'.\n".format(delay))
except:
    print("[Warning] Delay has been set to 0.3, since there's an invalid value on the config.\n")

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

keys = {"w": keyboard.VK_W, "a": keyboard.VK_A, "s": keyboard.VK_S, "d": keyboard.VK_D, "space": keyboard.VK_SPACE, "sneak": keyboard.VK_SHIFT, "mleft": keyboard.VK_LEFTCLICK, "mright": keyboard.VK_RIGHTCLICK}

keyspressed = {"w": False, "a": False, "s": False, "d": False, "space": False, "sneak": False, "mleft": False, "mright": False}
numberCode = {1: keyboard.VK_1, 2: keyboard.VK_2, 3: keyboard.VK_3, 4: keyboard.VK_4, 5: keyboard.VK_5, 6: keyboard.VK_6, 7: keyboard.VK_7, 8: keyboard.VK_8, 9: keyboard.VK_9}

global game_channel, started
started = False
game_channel = 0

async def walk(key):
    if (keyspressed.get(key)):
        keyboard.ReleaseKey(keys[key])
        keyspressed[key] = False
    else:
        keyboard.PressKey(keys[key])
        keyspressed[key] = True

@bot.event
async def on_ready():
    creator_user = await bot.fetch_user(310011769332695041)
    print("Bot Started Correctly\n")
    print(f"Bot name: {bot.user.name}")
    print(f"Bot id: {bot.user.id}")

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='!start |Made by: {}'.format(creator_user)), status='idle')



@bot.event
async def on_message(message):
    creator_user = await bot.fetch_user(310011769332695041)
    if message.channel.id == game_channel and started:
        user = message.author
        msg = message.content.lower()
        params = msg.split(" ")

        for x in range(0, len(params)):
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
            elif (params[x] == "inventory" or params[x] == "inventario" or params[x] == "e" or params[x] == "i"):
                keyboard.ClickKey(keyboard.VK_E)
            elif (params[x] == "esc"):
                keyboard.ClickKey(keyboard.VK_ESC)
            elif (params[x] == "f"):
                keyboard.ClickKey(keyboard.VK_F)

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

            elif (params[x] == ("pegar") or params[x] == ("romper") or params[x] == ("break") or params[x] == ("punch") or params[x] == ("mine") or params[x] == ("minar") or params[x] == ("destruir") or params[x] == ("picar") or "izquierdo" in params[x]):
                key = "mleft"
                if (keyspressed.get(key)):
                    keyspressed[key] = False
                else:
                    keyspressed[key] = True
                await mouse.leftclick(keyspressed.get(key))
            elif (params[x] == ("colocar") or params[x] == ("place") or params[x] == ("block") or params[x] == ("bloquear") or params[x] == ("protect") or params[x] == ("proteger") or "derecho" in params[x]):
                key = "mright"
                if (keyspressed.get(key)):
                    keyspressed[key] = False
                else:
                    keyspressed[key] = True
                await mouse.rightclick(keyspressed.get(key))

            await asyncio.sleep(delay)
    elif isinstance(message.channel, discord.channel.TextChannel):
        await bot.process_commands(message)

@bot.command(name="start", aliases=['empezar', 'comenzar', 'go'])
async def _start(ctx):
    global game_channel, started
    creator_user = await bot.fetch_user(310011769332695041)

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='!stop |Made by: {}'.format(creator_user)), status='online')
    started = True
    game_channel = ctx.channel.id

    embed = discord.Embed(title="Minigame Started!", colour=discord.Colour(0xff1f), description="The game has started. Remember to join the client to a voice channel, and Stream Minecraft. ")
    embed.set_footer(text=f"Bot made by: {creator_user}", icon_url=f"{creator_user.avatar_url}")
    embed.add_field(name="Not Working?", value="Try focusing Minecraft window. :sunglasses: ")
    await ctx.channel.send(embed=embed)

@bot.command(name="stop", aliases=['parar', 'disconnect', 'cancelar', 'cancel'])
async def _stop(ctx):
    global game_channel, started
    creator_user = await bot.fetch_user(310011769332695041)

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='!start |Made by: {}'.format(creator_user)), status='idle')
    started = False
    game_channel = int(0)

    embed = discord.Embed(title="Controller Finished!", colour=discord.Colour(0xff0000), description="Controller has been disconnected. No more Minecraft for today :rage:.")
    embed.set_footer(text=f"Bot made by: {creator_user}", icon_url=f"{creator_user.avatar_url}")
    await ctx.channel.send(embed=embed)



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    else:
        print(error)

try:
    bot.run(config.get("bot_token"))
except:
    print("Token is invalid or not set!\n")
    input("Press a key to close...")
