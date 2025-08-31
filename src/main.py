import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import asyncio

load_dotenv()
TOKEN = os.getenv("TOKEN")
COGS_DIR = os.path.join(os.path.dirname(__file__), "cogs")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True 

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado y funcionado {bot.user}')

    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} Slash Commands sincronizados")
    except Exception as e:
        print(e)


async def load_cogs():
    for filename in os.listdir(COGS_DIR):
        if filename.endswith(".py") and filename != '__init__.py':
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())