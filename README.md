# **PokeMaster — Tu Pokédex y Juego Pokémon en Discord**

**PokeMaster** es un bot de Discord inspirado en el mundo Pokémon.  
Permite **consultar información detallada de cualquier Pokémon**, **jugar partidas de adivinanza**, y **acceder a una guía interactiva de comandos**, todo mediante **slash commands** modernos y visuales.  

---

## 🚀 **Características**
- ✅ Consulta Pokémon por **nombre o número** usando la [PokeAPI](https://pokeapi.co/).  
- ✅ Juego de **“Adivina el Pokémon”** con pistas, intentos y límite de tiempo.  
- ✅ Sistema de **ayuda interactiva** con embeds explicativos.  
- ✅ **Colores, tipos y generaciones** personalizadas con emojis.  
- ✅ Uso completo de **slash commands (`/comandos`)**.  
- 💾 Lectura dinámica de datos desde archivos JSON locales.  

---

## 📜 **Comandos disponibles**

### 🎮 `/play`
Inicia el juego de adivinanza Pokémon.  
El bot seleccionará un Pokémon aleatorio y te mostrará **3 pistas** sobre él.  
Tendrás **3 intentos** y **1 minuto** para adivinar correctamente.

**Ejemplo de uso:**
```bash
/play
```

---

### 💬 `/answer <nombre>`
Responde con el nombre del Pokémon que crees correcto.  
- Si aciertas 🎉 → Ganas la partida y ves la imagen del Pokémon.  
- Si fallas ❌ → Pierdes una oportunidad (tienes 3 en total).  
- Si se acaba el tiempo ⏰ → El bot revelará la respuesta.  

**Ejemplo de uso:**
```bash
/answer pikachu
```

---

### 📖 `/pokedex <nombre o número>`
Consulta información detallada de cualquier Pokémon.  
Incluye:
- Tipo(s) y debilidades.  
- Peso y altura.  
- Región y generación.  
- Descripción oficial de la Pokédex (en español o inglés).  

**Ejemplo de uso:**
```bash
/pokedex charizard
```

---

### 🧠 `/help`
Muestra una guía completa con la descripción y funcionamiento de todos los comandos del bot.  
Ideal para nuevos usuarios.

**Ejemplo de uso:**
```bash
/help
```

---

## 📂 **Estructura del proyecto**

📦 **PokeMaster**  
┣ 📂 **data**  
┃ ┣ 📜 `color_pokemon.json` — Colores base de los Pokémon.  
┃ ┣ 📜 `generations.json` — Datos de generaciones y regiones.  
┃ ┗ 📜 `types_emojis.json` — Emojis asociados a tipos.  
┣ 📂 **env** — Entorno virtual (no subir a Git).  
┣ 📂 **image**  
┃ ┗ 📜 `pokeball.png` — Imagen usada en embeds.  
┣ 📂 **src**  
┃ ┣ 📂 **cogs**  
┃ ┃ ┣ 📜 `__init__.py` — Inicialización del módulo de comandos.  
┃ ┃ ┣ 📜 `game.py` — Lógica del juego “Adivina el Pokémon”.  
┃ ┃ ┣ 📜 `help.py` — Comando de ayuda interactivo.  
┃ ┃ ┗ 📜 `pokedex.py` — Comando para consultar Pokémon.  
┃ ┗ 📜 `main.py` — Archivo principal del bot.  
┣ 📜 `.env` — Contiene el token del bot (no subir a Git).  
┣ 📜 `.gitignore` — Archivos/carpetas ignoradas por Git.  
┣ 📜 `LICENSE` — Licencia del proyecto.  
┣ 📜 `README.md` — Documentación del proyecto.  
┗ 📜 `requirements.txt` — Dependencias del bot.  

---

## 🛠️ **Instalación**

1. **Clona este repositorio:**
   ```bash
   git clone https://github.com/tuusuario/pokemaster.git
   cd pokemaster
   ```

2. **Crea un entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # En Linux/Mac
   venv\Scripts\activate      # En Windows
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Crea un archivo `.env` con tu token de Discord:**
   ```bash
   TOKEN = 'tu_token_aqui'
   ```

5. **Ejecuta el bot:**
   ```bash
   python src/main.py
   ```

---

## 🧠 **Tecnologías usadas**
- Python 3.10+ 🐍  
- [discord.py (v2.x)](https://discordpy.readthedocs.io/)  
- [PokeAPI](https://pokeapi.co/)  
- JSON para persistencia de datos locales  

---

## 🎨 **Ejemplo de uso**
> **Jugador:** `/pokedex gengar`  
> **PokeMaster:** *Envía un embed con la descripción, tipo, generación y debilidades de Gengar.*  
>  
> **Jugador:** `/play`  
> **PokeMaster:** “Tienes 3 intentos para adivinar el Pokémon misterioso.”  

---

## 📄 **Licencia**
Este proyecto está bajo la licencia **MIT**, lo que significa que puedes usarlo, modificarlo y distribuirlo libremente siempre que mantengas el crédito correspondiente.
