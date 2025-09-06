import discord
from discord.ext import commands
from discord import app_commands
import requests
import random

URL = "https://pokeapi.co/api/v2/pokemon/"

class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="play",
        description="comando para comenzar un juego de adivinaza con el bot"
    )
    async def play(self, interaction: discord.Interaction):
        response = requests.get(URL + random.randint(1, 1000))

        if response.status_code == 200:
            data = response.json()
            # Peso y altura (directo)
            weight = data["weight"]
            height = data["height"]
            types = [t["type"]["name"] for t in data["types"]]
            ability = [h["ability"]["name"] for h in data["abilities"]]
            games = [g["version"]["name"] for g in data["game_indices"]]
            species_url = data["species"]["url"]
            species_data = requests.get(species_url).json()
            generation = species_data["generation"]["name"]

            # Ahora pedimos la generación y obtenemos la región
            gen_url = species_data["generation"]["url"]
            gen_data = requests.get(gen_url).json()
            region = gen_data["main_region"]["name"]

            # Armamos el array con todo
            pokemon_info = [{
                "weight": f"El pokemon pesa {weight}kg",
                "height": f"El pokemon mide {height}m de alto",
                "tipes": f"Es tipo: {types}",
                "games": f"Aparece en estos juegos: {weight}",
                "region": f"Su region es {region}",
                "ability": f"Tiene estas habilidades{weight}"
            }]

        embed = discord.Embed(
            title="Adivina el pokemon",
            description="TieneS 3 intentos para adivinar el pokemon",
            color=(0x800080)
        )
        embed.add_field(
                name="Pista1:",
                value=pokemon_info["weight"],
                inline=False
        )
        embed.add_field(
                name="Pista2:",
                value=pokemon_info["height"],
                inline=False
        )
        embed.add_field(
                name="Pista3:",
                value=pokemon_info["types"],
                inline=False
        )
        embed.set_footer(text="Datos obtenidos de la PokeAPI")
        
        await interaction.channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Game(bot))