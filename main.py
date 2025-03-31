import discord
from discord.ext import commands
import os
import copy
import webserver
from datetime import datetime

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

jugadores = {
    "Nuria": [0, 0, 0],
    "Carlota": [0, 0, 0],
    "Thais": [0, 0, 0],
    "Brandon": [0, 0, 0],
    "Angelo": [0, 0, 0],
    "Lidia": [0, 0, 0]
}

backup_jugadores = copy.deepcopy(jugadores)
historial = []


def hacer_backup():
    global backup_jugadores
    backup_jugadores = copy.deepcopy(jugadores)


@bot.command()
async def restaurar_backup(ctx):
    global jugadores
    jugadores = copy.deepcopy(backup_jugadores)
    await ctx.send("El backup ha sido restaurado con éxito.")


def calcular_victorias(resultados):
    ranking_points = [5, 4, 3, 2, 1, 0]
    resultados.sort(key=lambda x: x[1])
    pos = 0
    mensajes = []
    ganadores = set()

    while pos < len(resultados):
        current_intentos = resultados[pos][1]
        grupo = []
        inicio = pos
        while pos < len(resultados) and resultados[pos][1] == current_intentos:
            grupo.append(resultados[pos][0])
            pos += 1

        posiciones = list(range(inicio, pos))
        suma = sum(ranking_points[i] for i in posiciones)
        promedio = suma / len(grupo)

        for jugador in grupo:
            jugadores[jugador][0] += promedio
            mensajes.append(f"{jugador} recibe {promedio:.2f} puntos de victoria por {current_intentos} intentos.")

        if inicio == 0:
            ganadores.update(grupo)

    for ganador in ganadores:
        jugadores[ganador][2] += 1

    return mensajes


def tabla_puntuaciones():
    header = "```TABLA DE PUNTUACIONES\n"
    header += "-" * 50 + "\n"
    header += "{:<10} | {:>8} | {:>10} | {:>10}\n".format("Jugador", "Puntos", "Intentos", "Victorias")
    header += "-" * 50 + "\n"
    lines = []
    for jugador, datos in sorted(jugadores.items(), key=lambda x: -x[1][0]):
        lines.append("{:<10} | {:>8.2f} | {:>10.2f} | {:>10.2f}".format(jugador, datos[0], datos[1], datos[2]))
    table = header + "\n".join(lines) + "\n" + "-" * 50 + "```"

    historial_str = "\n".join(historial[-5:])  # Mostrar solo los últimos 5 registros
    return f"{historial_str}\n\n{table}"


@bot.command()
async def ver_puntuaciones(ctx):
    await ctx.send(tabla_puntuaciones())


@bot.command()
async def puntuar(ctx, *, entrada: str):
    global jugadores, historial
    hacer_backup()

    tokens = entrada.split(",")
    resultados = []
    registro = datetime.now().strftime("%d/%m/%y") + "- "

    for token in tokens:
        token = token.strip()
        partes = token.split(" ")
        if len(partes) != 2:
            await ctx.send(f"Formato inválido '{token}'")
            return
        nombre, intentos_str = partes
        if nombre not in jugadores:
            await ctx.send(f"El jugador '{nombre}' no existe.")
            return
        try:
            intentos = int(intentos_str)
        except ValueError:
            await ctx.send(f"El número de intentos para '{nombre}' no es válido.")
            return
        puntos = intentos - 4
        jugadores[nombre][1] += puntos
        resultados.append((nombre, intentos))
        registro += f"{nombre[0].upper()}: {intentos} | "

    historial.append(registro.strip(" | "))
    mensajes_victoria = calcular_victorias(resultados)
    mensaje = "\n".join(mensajes_victoria)
    tabla = tabla_puntuaciones()
    await ctx.send(mensaje + "\n" + tabla)


@bot.command()
async def borrar(ctx):
    global jugadores, historial
    hacer_backup()
    jugadores = {nombre: [0, 0, 0] for nombre in jugadores}
    historial.clear()
    await ctx.send("Todas las puntuaciones han sido reiniciadas.")


@bot.command()
async def borrar_jugador(ctx, nombre: str):
    global jugadores
    if nombre in jugadores:
        hacer_backup()
        jugadores[nombre] = [0, 0, 0]
        await ctx.send(f"Las puntuaciones de {nombre} han sido reiniciadas.")
    else:
        await ctx.send(f"El jugador '{nombre}' no existe.")


@bot.event
async def on_ready():
    print(f'Corriendo... {bot.user}')


webserver.keep_alive()
bot.run(DISCORD_TOKEN)
