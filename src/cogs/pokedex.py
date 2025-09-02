import discord
from discord.ext import commands
from discord import app_commands
import requests
import json
import os

PATH_JSON = os.path.abspath("data")
URL = "https://pokeapi.co/api/v2/pokemon/"
SPECIES_URL = "https://pokeapi.co/api/v2/pokemon-species/"
TYPE_URL = "https://pokeapi.co/api/v2/type/"

colores_pokemon = {
    "red": 0xFF0000,
    "blue": 0x0000FF,
    "green": 0x00FF00,
    "yellow": 0xFFFF00,
    "black": 0x000000,
    "brown": 0x8B4513,
    "purple": 0x800080,
    "pink": 0xFFC0CB,
    "gray": 0x808080,
    "white": 0xFFFFFF
}

with open(PATH_JSON + "/types_emojis.json", "r", encoding="utf-8") as f:
    types_emojis = json.load(f)

class Pokedex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="pokedex",
        description="Escribe el nombre o numero de un pokemon"
    )
    async def pokedex(self, interaction: discord.interactions, *, name: str):
        response = requests.get(URL + name.lower())
        if response.status_code == 200:
            data = response.json()

            # Petición extra: species (para región, color y descripción)
            species_response = requests.get(SPECIES_URL + str(data["id"]))
            region = "Desconocida"
            color = "Desconocido"
            
            descripcion = "Sin descripción disponible."
            if species_response.status_code == 200:
                species_data = species_response.json()
                region = species_data["generation"]["name"]
                color = species_data["color"]["name"]

            # Buscar descripción en español, si no existe usar inglés
            for entry in species_data["flavor_text_entries"]:
                if entry["language"]["name"] == "es":
                    descripcion = entry["flavor_text"].replace("\n", " ").replace("\f", " ")
                    break
            else:  # Si no hay en español, usa inglés
                for entry in species_data["flavor_text_entries"]:
                    if entry["language"]["name"] == "en":
                        descripcion = entry["flavor_text"].replace("\n", " ").replace("\f", " ")
                        break
            color_embed = colores_pokemon.get(color.lower(), 0xFF0000)

            # Datos básicos
            name_poke = data["name"].capitalize()
            poke_id = data["id"]
            types = [t["type"]["name"] for t in data["types"]]
            types_str = ", ".join([f"{types_emojis.get(t, '')} {t.capitalize()}" for t in types])
            weight = data["weight"]
            height = data["height"]
            imagen = data["sprites"]["front_default"]

            # weaknesses
            weaknesses = set()
            for tipo in types:
                type_response = requests.get(TYPE_URL + tipo)
                if type_response.status_code == 200:
                    type_data = type_response.json()
                    for weakness in type_data["damage_relations"]["double_damage_from"]:
                        weaknesses.add(weakness["name"])
            weaknesses_str = ", ".join([f"{types_emojis.get(w, '')} {w.capitalize()}" for w in weaknesses]) if weaknesses else "Ninguna"

            # Embed de Discord
            embed = discord.Embed(
                title="{} (#{:04})".format(name_poke, poke_id),
                description=f"{descripcion}\n\nGeneracion: **{region.capitalize()}**",
                color=color_embed
            )

            embed.add_field(name="Tipos", value=types_str, inline=True)
            embed.add_field(name="Altura", value=f"{height}m", inline=True)
            embed.add_field(name="Peso", value=f"{weight}kg", inline=True)
            embed.add_field(name="weaknesses", value=weaknesses_str, inline=False)
            embed.set_thumbnail(url=imagen)
            embed.set_footer(text="Datos obtenidos de la PokeAPI")

            await interaction.channel.send(embed=embed)
        
        else: 
            await interaction.channel.send("No se encontro el pokemon")

async def setup(bot):
    await bot.add_cog(Pokedex(bot))