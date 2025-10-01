# ConexoBot

**ConexoBot** es un bot de Discord para gestionar puntuaciones de jugadores en partidas, con historial de juegos, cálculo automático de victorias y comandos para administrar jugadores y rankings.

## Características

- Registrar puntos de jugadores en partidas.  
- Visualizar tabla de puntuaciones y ranking actualizado.  
- Reiniciar puntuaciones de todos los jugadores o de jugadores individuales.  
- Restaurar backups automáticos antes de cambios importantes.  
- Historial de partidas recientes.  
- Fácil de configurar y ejecutar en tu servidor de Discord.  

## Comandos

| Comando | Descripción |
|---------|-------------|
| `/puntuar <jugador intentos, ...>` | Puntúa a los jugadores en la partida. Ejemplo: `/puntuar Nuria 5, Carlota 7` |
| `/ver_puntuaciones` | Muestra la tabla de puntuaciones y el historial de las últimas partidas. |
| `/borrar` | Reinicia todas las puntuaciones y el historial. |
| `/borrar_jugador <nombre>` | Reinicia la puntuación de un jugador específico. |
| `/restaurar_backup` | Restaura el último backup de puntuaciones. |

## Instalación

1. Clona el repositorio:  
```bash
git clone https://github.com/nuriabravo/conexobot.git
cd conexobot
```

2. Instala dependencias:
```bash
pip install -r requirements.txt
```

3. Configura las variables de entorno en un archivo .env:
```bash
DISCORD_TOKEN=tu_token_aqui
```

4. Ejecuta el bot:
```bash
python main.py
```
