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
        description="Comando para comenzar un juego de adivinanza con el bot"
    )
    async def play(self, interaction: discord.Interaction):
        response = requests.get(URL + str(random.randint(1, 1000)))

        if response.status_code == 200:
            data = response.json()
            correct_name = data["name"]
            weight = data["weight"]
            height = data["height"]
            types = [t["type"]["name"] for t in data["types"]]
            ability = [h["ability"]["name"] for h in data["abilities"]]
            games = [g["version"]["name"] for g in data["game_indices"]]
            species_url = data["species"]["url"]
            species_data = requests.get(species_url).json()
            imagen = data["sprites"]["front_default"]
            generation = species_data["generation"]["name"]

            gen_url = species_data["generation"]["url"]
            gen_data = requests.get(gen_url).json()
            region = gen_data["main_region"]["name"]

            pokemon_info = {
                "weight": f"El pokemon pesa {weight}kg",
                "height": f"El pokemon mide {height}m de alto",
                "types": f"Es tipo: {', '.join(types)}",
                "games": f"Aparece en estos juegos: {', '.join(games[:5])}",
                "region": f"Su región es {region}",
                "ability": f"Tiene estas habilidades: {', '.join(ability)}"
            }

            embed = discord.Embed(
                title="Adivina el Pokémon",
                description="Tienes 3 intentos para adivinar el Pokémon",
                color=0x800080
            )
            embed.add_field(name="pokemon:", value=f"{correct_name}", inline=False)
            embed.add_field(name="Pista 1:", value=pokemon_info["weight"], inline=False)
            embed.add_field(name="Pista 2:", value=pokemon_info["height"], inline=False)
            embed.add_field(name="Pista 3:", value=pokemon_info["types"], inline=False)
            embed.set_footer(text="Datos obtenidos de la PokeAPI")

            await interaction.response.send_message(embed=embed)
            return [correct_name, imagen]
        else:
            await interaction.response.send_message("No se pudo obtener información del Pokémon.")
    
    @app_commands.command(
        name='answer',
        description='Responde con el nombre del pokemon'
    )
    async def answer(self, interaction: discord.Interaction, *, name: str):
        data = Game.play() 
        if name == data[0]:
            embed = discord.Embed(
                title="Correcto el pokemon era: {}".format(name),
                description="Ere todo un maestro pokemon",
                color=0x800080
            )
            embed.set_image(data[1])
            embed.set_footer(text="Datos obtenidos de la PokeAPI")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Lo siento pero no es l pokemon correcto.")


async def setup(bot):
    await bot.add_cog(Game(bot))
