import discord
from discord.ext import commands
from discord import app_commands
import os


URL = "https://pokeapi.co/api/v2/pokemon/"
IMG = os.path.abspath("image/pokeball.png")

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(
        name="help",
        description="Comando de ayuda para usar el bot"
    )
    async def help_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📘 Guía de Comandos Pokémon",
            description=(
                "Aquí tienes una explicación de cómo funcionan los comandos disponibles "
                "para interactuar con la **PokeAPI** y jugar al **Adivina el Pokémon**."
            ),
            color=0x800080
        )

        embed.add_field(
            name="🎮 `/play` — Inicia el juego de adivinanza",
            value=(
                "Este comando comienza un nuevo juego de **Adivina el Pokémon**.\n"
                "El bot elegirá un Pokémon al azar y te mostrará **3 pistas** sobre él.\n"
                "Tendrás **3 intentos** y **1 minuto** para adivinar correctamente el nombre.\n\n"
                "⚠️ Si ya hay un juego activo, deberás esperar a que termine antes de comenzar otro."
            ),
            inline=False
        )

        embed.add_field(
            name="💬 `/answer <nombre>` — Responde con tu adivinanza",
            value=(
                "Usa este comando para intentar adivinar el Pokémon.\n"
                "Si aciertas, el bot mostrará su imagen y confirmará tu victoria 🎉.\n"
                "Si fallas, perderás una oportunidad (tienes 3 en total).\n\n"
                "Cuando se acaben tus intentos o el tiempo, el bot revelará el nombre correcto."
            ),
            inline=False
        )

        embed.add_field(
            name="📖 `/pokedex <nombre o número>` — Consulta información de un Pokémon",
            value=(
                "Este comando muestra información detallada del Pokémon que elijas.\n"
                "Incluye:\n"
                "• Su tipo y debilidades\n"
                "• Peso y altura\n"
                "• Región y generación\n"
                "• Descripción del Pokédex en español o inglés\n\n"
                "Los datos se obtienen directamente desde la **PokeAPI**."
            ),
            inline=False
        )

        file = discord.File(IMG, filename="pokeball.png")
        embed.set_thumbnail(url="attachment://pokeball.png")
        embed.set_footer(text="Datos obtenidos de la PokeAPI")

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))