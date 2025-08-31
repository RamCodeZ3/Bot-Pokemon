import discord
from discord.ext import commands
from discord import app_commands
import requests

URL = "https://pokeapi.co/api/v2/pokemon/"
SPECIES_URL = "https://pokeapi.co/api/v2/pokemon-species/"

class Pokedex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="pokedex",
        description="Escribe el nombre o numero de un pokemon"
    )
    async def pokedex(self, interaction: discord.interactions, *, name: str):
        respose = requests.get(URL + name.lower())
        if respose.status_code == 200:
            data = respose.json()
            species_response = requests.get(SPECIES_URL + str(data["id"]))
            region = "Desconocida"
        
        if species_response.status_code == 200:
            species_data = species_response.json()
            region = species_data["generation"]["name"]

            # Extraemos los datos
            nombre = data["name"].capitalize()
            poke_id = data["id"]
            tipos = ", ".join([t["type"]["name"] for t in data["types"]])
            peso = data["weight"]
            altura = data["height"]
            imagen = data["sprites"]["front_default"]

            # Creamos un Embed para Discord
            embed = discord.Embed(
                title=f"{nombre} (#{poke_id})",
                description=f"Región de origen: **{region.capitalize()}**",
                color=discord.Color.blue()
            )
            embed.add_field(name="Tipos: ", value=tipos, inline=False)
            embed.add_field(name="Altura: ", value=altura, inline=False)
            embed.add_field(name="Peso: ", value=peso, inline=False)
            embed.set_thumbnail(url=imagen)
            await interaction.response.send_message(embed=embed)
        
        else: 
            await interaction.channel.send("No se encontro el pokemon")

async def setup(bot):
    await bot.add_cog(Pokedex(bot))