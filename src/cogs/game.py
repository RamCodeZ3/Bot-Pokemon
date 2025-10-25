import discord
from discord.ext import commands
from discord import app_commands
import requests
import random
import asyncio
import os


URL = "https://pokeapi.co/api/v2/pokemon/"
IMG = os.path.abspath("image/pokeball.png")


class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pokemon = None
        self.image = None
        self.time_limit = 60
        self.game_active = False
        self.opportunities = 3
        self.timer_task = None
    
    async def timer(self, interaction: discord.Interaction):
        await asyncio.sleep(self.time_limit)
        if self.game_active:
            self.game_active = False
            embed = discord.Embed(
                title="¡Se acabó el tiempo!",
                description=f"El Pokémon era **{self.pokemon}**.",
                color=0x800080
            )

            embed.set_thumbnail(url=self.image)
            embed.set_footer(text="Tiempo límite: 1 minuto")
            await interaction.followup.send(embed=embed)

    @app_commands.command(
        name="play",
        description="Comando para comenzar un juego de adivinanza con el bot"
    )
    async def play(self, interaction: discord.Interaction):
        if self.game_active:
            await interaction.response.send_message("Ya hay un juego activo. Termina el anterior antes de comenzar otro.")
            return
        
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
                f"El pokemon pesa {weight / 10:.1f}kg",
                f"El pokemon mide {height / 10:.1f}m de alto",
                f"Es tipo: {', '.join(types)}",
                f"Aparece en estos juegos: {', '.join(games[:5])}",
                f"Su región es {region}",
                f"Tiene estas habilidades: {', '.join(ability)}"
            ]
            # Actualizacion de las opotunidades y la activacion del juego
            self.opportunities = 3
            self.game_active = True

            embed = discord.Embed(
                title="Adivina el Pokémon",
                description="Tienes 3 intentos y un minuto para adivinar el Pokémon",
                color=0x800080
            )
            
            embed.add_field(
                name="pokemon:",
                value=f"{self.pokemon}",
                inline=False
            )
            
            for i, hint in enumerate(random.sample(pokemon_info, 3), start=1):
                embed.add_field(name=f"Pista {i}:", value=hint, inline=False)
            
            file = discord.File(IMG, filename="pokeball.png")
            embed.set_thumbnail(url="attachment://pokeball.png")
            embed.set_footer(text="Datos obtenidos de la PokeAPI")

            await interaction.response.send_message(embed=embed, file=file)
            self.timer_task = asyncio.create_task(self.timer(interaction))
        else:
            await interaction.response.send_message("No se pudo obtener información del Pokémon.")

    @app_commands.command(
        name='answer',
        description='Responde con el nombre del pokemon'
    )
    async def answer(self, interaction: discord.Interaction, *, name: str):
        if name == self.pokemon and self.opportunities != 0 and self.game_active:
            embed = discord.Embed(
                title="Correcto el pokemon era: {}".format(name),
                description="Ere todo un maestro pokemon",
                color=0x800080
            )
            embed.set_thumbnail(url=self.image)
            embed.set_footer(text="Datos obtenidos de la PokeAPI")
            self.game_active = False
            await interaction.response.send_message(embed=embed)
        
        elif self.opportunities == 0:
            embed = discord.Embed(
                title="El pokemon correcto era: {}".format(self.pokemon),
                description="Talvez a la proxima lo adivine",
                color=0x800080
            )
            embed.set_thumbnail(url=self.image)
            embed.set_footer(text="Datos obtenidos de la PokeAPI")
            self.game_active = False
            await interaction.response.send_message(embed=embed)
        
        if self.game_active != True: await interaction.response.send_message('No hay pokemon para adivinar')

        else:
            await interaction.response.send_message(
                "Lo siento pero no es el pokemon correcto. te quedan {} oportunidades"
                .format(self.opportunities)
            )
            self.opportunities -= 1

async def setup(bot):
    await bot.add_cog(Game(bot))
