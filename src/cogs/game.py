import discord
from discord.ext import commands
from discord import app_commands
import requests
import random
import asyncio
import os


URL = "https://pokeapi.co/api/v2/pokemon/"
IMG = os.path.abspath("image/pokeball.png")

async def timer():
    await asyncio.sleep(5)
    return False

class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pokemon = None
        self.image = None
        self.time = timer()
        self.opportunities = 3

    @app_commands.command(
        name="play",
        description="Comando para comenzar un juego de adivinanza con el bot"
    )
    async def play(self, interaction: discord.Interaction):
        response = requests.get(URL + str(random.randint(1, 1000)))

        if response.status_code == 200:
            data = response.json()
            self.pokemon = data["name"]
            weight = data["weight"]
            height = data["height"]
            types = [t["type"]["name"] for t in data["types"]]
            ability = [h["ability"]["name"] for h in data["abilities"]]
            games = [g["version"]["name"] for g in data["game_indices"]]
            species_url = data["species"]["url"]
            species_data = requests.get(species_url).json()
            self.image = data["sprites"]["front_default"]
            generation = species_data["generation"]["name"]

            gen_url = species_data["generation"]["url"]
            gen_data = requests.get(gen_url).json()
            region = gen_data["main_region"]["name"]

            pokemon_info = [
                f"El pokemon pesa {weight}kg",
                f"El pokemon mide {height}m de alto",
                f"Es tipo: {', '.join(types)}",
                f"Aparece en estos juegos: {', '.join(games[:5])}",
                f"Su región es {region}",
                f"Tiene estas habilidades: {', '.join(ability)}"
            ]

            embed = discord.Embed(
                title="Adivina el Pokémon",
                description="Tienes 3 intentos para adivinar el Pokémon",
                color=0x800080
            )
            embed.add_field(name="pokemon:", value=f"{self.pokemon}", inline=False)
            embed.add_field(name="Pista 1:", value=pokemon_info[random.randint(0, 1)], inline=False)
            embed.add_field(name="Pista 2:", value=pokemon_info[random.randint(2, 3)], inline=False)
            embed.add_field(name="Pista 3:", value=pokemon_info[random.randint(4, 5)], inline=False)
            file = discord.File(IMG, filename="pokeball.png")
            embed.set_thumbnail(url="attachment://pokeball.png")
            embed.set_footer(text="Datos obtenidos de la PokeAPI")

            await interaction.response.send_message(embed=embed, file=file)
        else:
            await interaction.response.send_message("No se pudo obtener información del Pokémon.")

    @app_commands.command(
        name='answer',
        description='Responde con el nombre del pokemon'
    )
    async def answer(self, interaction: discord.Interaction, *, name: str):
        if name == self.pokemon and self.opportunities != 0 and self.time:
            embed = discord.Embed(
                title="Correcto el pokemon era: {}".format(name),
                description="Ere todo un maestro pokemon",
                color=0x800080
            )
            embed.set_image(url=self.image)
            embed.set_footer(text="Datos obtenidos de la PokeAPI")
            await interaction.response.send_message(embed=embed)
        
        elif self.opportunities == 0:
            embed = discord.Embed(
                title="El pokemon correcto era: {}".format(self.pokemon),
                description="Talvez a la proxima lo adivine",
                color=0x800080
            )
            embed.set_image(url=self.image)
            embed.set_footer(text="Datos obtenidos de la PokeAPI")
            await interaction.response.send_message(embed=embed)
        
        else:
            await interaction.response.send_message("Lo siento pero no es el pokemon correcto. te quedan {} oportunidades".format(self.opportunities))
            self.opportunities -= 1

async def setup(bot):
    await bot.add_cog(Game(bot))
