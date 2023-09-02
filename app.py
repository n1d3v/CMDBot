import discord
import subprocess
import psutil  # Import the psutil library
from discord.ext import commands
import os
import sys
import time

# Your bot's token
TOKEN = 'your bot token here'

# Initialize the bot with intents
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

# Performance monitoring parameters
CPU_THRESHOLD = 75 # Define the CPU usage threshold (in percentage)
MEMORY_THRESHOLD = 50  # Define the memory usage threshold (in percentage)
RESTART_DELAY = 10  # Define the delay before restarting (in seconds)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.command()
async def sendcmd(ctx, *, command):
    # Check if the command starts with '!' (security check)
    if command.startswith('!'):
        await ctx.send('Invalid command. Please do not use "!".')
        return
    
    # Check if the command contains 'curl' (or any other blocked command)
    if 'curl' in command.lower():
        await ctx.send('The `curl` command is blocked.')
        return

    try:
        # Execute the command in a CMD prompt
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        await ctx.send(f'Command executed successfully:\n```{result}```')
    except subprocess.CalledProcessError as e:
        await ctx.send(f'Error executing the command:\n```{e.output}```')
    except Exception as e:
        await ctx.send(f'An error occurred:\n```{str(e)}```')

# Performance monitoring function
def monitor_performance():
    while True:
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent

        # Check if CPU or memory usage exceeds the threshold
        if cpu_percent > CPU_THRESHOLD or memory_percent > MEMORY_THRESHOLD:
            print(f'Performance spike detected (CPU: {cpu_percent}%, Memory: {memory_percent}%)')
            restart_bot()
            break

        time.sleep(10)  # Check every 10 seconds

# Bot restart function
def restart_bot():
    # Delay before restarting
    time.sleep(RESTART_DELAY)
    
    # Restart the bot by launching a new instance of the Python script
    python_executable = sys.executable
    os.execl(python_executable, python_executable, *sys.argv)

if __name__ == "__main__":
    # Start the performance monitoring loop in a separate thread
    import threading
    performance_monitoring_thread = threading.Thread(target=monitor_performance)
    performance_monitoring_thread.start()

    # Run the bot
    bot.run(TOKEN)
