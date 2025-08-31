import discord
from discord.ext import commands
from discord import app_commands

class Pokedex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="pokedex",
        description="Escribe el nombre o numero de un pokemon"
    )
    async def pokedex(self, interaction: discord.interactions):
        await interaction.channel.send("Hola prueba de text")

async def setup(bot):
    await bot.add_cog(Pokedex(bot))