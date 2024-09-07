import discord
from discord.ext import commands
from discord.ui import View
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.AutoShardedBot(command_prefix=">>", intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="games 🎮"))
    
    extensions = [
        "menu",
        "tictactoe"
    ]

    for ext in extensions:
        try:
            await bot.load_extension(f"cogs.{ext}")
            print(f"Loaded extension: {ext}")
        except commands.ExtensionError as e:
            print(f"Failed to load extension {ext}: {e}")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


if TOKEN is None:
    print("Error: Discord bot TOKEN not found in the .env file.")
else:
    bot.run(TOKEN)