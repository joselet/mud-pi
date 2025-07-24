#!/usr/bin/env python

import time
import os
import json  # Puedes usar `yaml` si prefieres archivos YAML
from mudserver import MudServer
from sistema_de_combate import iniciar_combate, procesar_turno_combate

# Carpeta donde están almacenadas las salas
ROOMS_DIR = "rooms"
# Carpeta donde se almacenan las fichas de los jugadores
PLAYERS_DIR = "players"

# Cache para las salas cargadas
rooms_cache = {}

# Función para cargar una sala desde un archivo
def load_room(room_name):
    # Si la sala ya está en la caché, devolverla
    if room_name in rooms_cache:
        return rooms_cache[room_name]
    
    # room_file = os.path.join(ROOMS_DIR, f"{room_name.lower()}.json")
    # if not os.path.isfile(room_file):
    #     raise ValueError(f"Room file not found: {room_file}")

    # Convertir el nombre de la sala en una ruta relativa
    room_file = os.path.join(ROOMS_DIR, *room_name.lower().split("/")) + ".json"
    
    if not os.path.isfile(room_file):
        raise ValueError(f"Room file not found: {room_file}")
        
    # Cargar la sala desde el archivo
    with open(room_file, "r", encoding="utf-8") as file:
        room_data = json.load(file)
    
    # Verificar que la sala tiene los campos obligatorios
    required_keys = {"title", "description", "exits"}
    if not required_keys.issubset(room_data.keys()):
        raise ValueError(f"Room file '{room_path}' is missing required keys: {required_keys - room_data.keys()}")
    
    # Almacenar en la caché y devolver
    rooms_cache[room_name] = room_data
    return room_data

def move_player(id, exit_name):
    try:
        room = load_room(players[id]["room"])
        ex = exit_name.lower()
        if ex in room["exits"]:
            current_room = players[id]["room"]  # Store the current room before moving
            # Notificar salida al resto de jugadores en la sala actual
            for pid, pl in players.items():
                if players[pid]["room"] == current_room and pid != id:
                    mud.send_message(pid, f"{players[id]['name']} se fue hacia '{ex}'")
            
            # Mover al jugador
            players[id]["room"] = room["exits"][ex]
            new_room = players[id]["room"]  # Store the new room after moving
            
            # Determinar la salida que lleva al current_room desde la nueva sala
            reverse_exit = next((exit_name for exit_name, target_room in load_room(new_room)["exits"].items() if target_room == current_room), "algún lugar desconocido")
            
            # Notificar llegada al resto de jugadores en la nueva sala
            for pid, pl in players.items():
                if players[pid]["room"] == new_room and pid != id:
                    mud.send_message(pid, f"{players[id]['name']} llega desde '{reverse_exit}'")
            
            # Mostrar la sala al jugador usando la función ya existente
            mostrar_sala_al_jugador(id)
        else:
            mud.send_message(id, f"Salida desconocida '{ex}'")
    except ValueError as e:
        print(f"[ERR] Error loading room (pid= {id}): {e}")  # Debug por salida estándar
        mud.send_message(id, "\033[31mHas sufrido un fallo espacio/tiempo y apareces en la incubadora.\033[0m")
        players[id]["room"] = "respawn"
        mostrar_sala_al_jugador(id)

def cargar_o_crear_ficha(nombre, password):
    player_file = os.path.join(PLAYERS_DIR, f"{nombre.lower()}.json")
    if os.path.isfile(player_file):
        with open(player_file, "r") as file:
            ficha = json.load(file)
        if ficha["password"] != password:
            raise ValueError("Contraseña incorrecta.")
    else:
        ficha = {
            "name": nombre,
            "password": password,
            "vida": 100,
            "energia": 100,
            "fuerza": 10,
            "destreza": 10,
            "magia": 5,
            "carisma": 5,
            "suerte": 5,
            "room": "inicio"  # Nueva clave para la sala inicial
        }
        with open(player_file, "w") as file:
            json.dump(ficha, file)
    return ficha

def mostrar_sala_al_jugador(id):
    try:
        room = load_room(players[id]["room"])
        mud.send_message(id, room["title"])
        mud.send_message(id, room["description"])
        print(f"[LOG] (pid= {id}): {room["title"]}")  # Debug por salida estándar
        # Mostrar jugadores presentes en la nueva sala (excluyendo al jugador actual)
        players_here = [pl["name"] for pid, pl in players.items() if players[pid]["room"] == players[id]["room"] and pid != id]
        if players_here:
            mud.send_message(id, f"Aquí ves a: {', '.join(players_here)}")
        else:
            mud.send_message(id, "Estás solo aquí.")
        mud.send_message(id, f"Salidas: {', '.join(room['exits'])}")
    except ValueError as e:
        print(f"[ERR] Error loading room (pid= {id}): {e}")  # Debug por salida estándar
        mud.send_message(id, "\033[31mHas sufrido un fallo espacio/tiempo y apareces en la incubadora.\033[0m")
        players[id]["room"] = "respawn"
        mostrar_sala_al_jugador(id)


# Stores the players in the game
players = {}

# Start the server
mud = MudServer()

# Main game loop
while True:
    time.sleep(0.2)
    mud.update()

    for id in mud.get_new_players():
        # Initialize the player with proper flags
        players[id] = {"name": None, "room": None, "awaiting_name": True}
        mud.send_message(id, "Qué nombre tiene tu personaje?")  # Ask for the name once

    for id in mud.get_disconnected_players():
        if id not in players:
            continue
        # Guardar la sala actual en la ficha antes de eliminar al jugador
        ficha = players[id].get("ficha")
        if ficha:
            ficha["room"] = players[id]["room"]
            player_file = os.path.join(PLAYERS_DIR, f"{ficha['name'].lower()}.json")
            with open(player_file, "w") as file:
                json.dump(ficha, file)
        # Notificar a todos los jugadores que alguien ha salido
        for pid, pl in players.items():
            if pid != id:
                mud.send_message(pid, f"{players[id]['name']} salió del juego.")
        del players[id]

    for id, command, params in mud.get_commands():
        if id not in players:
            continue

        if players[id]["awaiting_name"]:
            # Handle name input
            player_name = command.strip()
            players[id]["name"] = player_name
            players[id]["awaiting_name"] = False
            players[id]["awaiting_password"] = True
            players[id]["password_attempts"] = 0  # Initialize password attempts
            player_file = os.path.join(PLAYERS_DIR, f"{player_name.lower()}.json")
            if os.path.isfile(player_file):
                mud.send_message(id, "Personaje encontrado. Dame la contraseña:")
            else:
                mud.send_message(id, "Personaje no encontrado. Vamos a crearlo. Por favor, establece una contraseña:")

        elif players[id].get("awaiting_password"):
            # Step 2: Handle password input with retry mechanism
            try:
                password = command.strip()
                players[id]["ficha"] = cargar_o_crear_ficha(players[id]["name"], password)
                # Usar la última sala guardada si existe, si no, "inicio"
                ficha_room = players[id]["ficha"].get("room", "inicio")
                players[id]["room"] = ficha_room
                players[id]["awaiting_password"] = False
                mud.send_message(id, f"Bienvenido al juego, {players[id]['name']}. Escribe 'ayuda' para obtener una lista de comandos.")
                mostrar_sala_al_jugador(id)
                # Notificar a todos los jugadores que alguien ha entrado
                for pid, pl in players.items():
                    if pid != id:
                        mud.send_message(pid, f"[info] {players[id]['name']} entró al juego.")
                # Notificar a los jugadores de la sala actual que alguien acaba de aparecer
                for pid, pl in players.items():
                    if players[pid]["room"] == players[id]["room"] and pid != id:
                        mud.send_message(pid, f"{players[id]['name']} acaba de aparecer en la sala por arte de magia.")
                # Mostrar por salida estándar para el log del servidor
                print(f"[LOG] {players[id]['name']} entró al juego (id={id})")
            except ValueError as e:
                players[id]["password_attempts"] += 1
                if players[id]["password_attempts"] >= 3:
                    mud.send_message(id, "Too many failed attempts. Disconnecting.")
                    mud._handle_disconnect(id)
                    del players[id]
                else:
                    mud.send_message(id, f"Error: {e}. Please try again ({3 - players[id]['password_attempts']} attempts left).")

        elif command == "ayuda":
            mud.send_message(id, "Commands:")
            mud.send_message(id, "  decir <message>  - Decir algo en voz alta, e.g. 'decir Hola a todos'")
            mud.send_message(id, "  mirar          - Examina tu alrededor, e.g. 'mirar'")
            mud.send_message(id, "  ir <exit>      - Mover hacia la salida especificada, e.g. 'ir outside'")
            mud.send_message(id, "  <exit>         - Atajo para moverse a la salida indicada, e.g. 'outside'")
            mud.send_message(id, "  estado         - Comprobar el estado de tu personaje")
            mud.send_message(id, "  matar <objetivo> - Atacar a otro personaje")
            mud.send_message(id, "  salir          - Abandonar el juego")
        elif command == "decir":
            for pid, pl in players.items():
                if players[pid]["room"] == players[id]["room"]:
                    mud.send_message(pid, f"{players[id]['name']} dice: {params}")

        elif command == "mirar":
            mostrar_sala_al_jugador(id)

        elif command == "ir":
            move_player(id, params)
        elif command == "salir":
            mud.send_message(id, "Desconectando. Adiós!")
            # Guardar la sala actual en la ficha antes de eliminar al jugador
            ficha = players[id].get("ficha")
            if ficha:
                ficha["room"] = players[id]["room"]
                player_file = os.path.join(PLAYERS_DIR, f"{ficha['name'].lower()}.json")
                with open(player_file, "w") as file:
                    json.dump(ficha, file)
            # Notificar al resto de jugadores que alguien ha salido
            for pid, pl in players.items():
                if pid != id:
                    mud.send_message(pid, f"[info] {players[id]['name']} se marchó del juego.")
            # Mostrar por salida estándar para el log del servidor
            print(f"[LOG] {players[id]['name']} salió del juego (id={id})")
            mud._handle_disconnect(id)
            if id in players:
                del players[id]
        elif command == "estado":
            ficha = players[id]["ficha"]
            mud.send_message(id, f"Estado actual: "
                                 f"\nVida: {ficha['vida']},       Energía: {ficha['energia']}, "
                                 f"\nFuerza: {ficha['fuerza']},      Destreza: {ficha['destreza']}, "
                                 f"\nMagia: {ficha['magia']}, Carisma: {ficha['carisma']}, Suerte: {ficha['suerte']}")
        elif command == "matar":
            # Generar un array con los jugadores en la sala (excluyendo al jugador actual)
            players_here = [pl["name"].strip().lower() for pid, pl in players.items() 
                            if players[pid]["room"] == players[id]["room"] and pid != id]
            
            # Debug: Mostrar jugadores en la sala
            #mud.send_message(id, f"Debug: Players in the room (array): {players_here}")
            #mud.send_message(id, f"Debug: Players structure: {players}")  # Mostrar toda la estructura de players
            #mud.send_message(id, f"Debug: Target victim (raw): '{params}'")
            #mud.send_message(id, f"Debug: Target victim (processed): '{params.strip().lower()}'")
            #mud.send_message(id, f"Debug: Target victim length: {len(params.strip())}")

            # Asignar target_name y mostrar su valor
            target_name = params.strip().lower()
            #mud.send_message(id, f"Debug: Final target_name: '{target_name}'")

            # Debug: Evaluar las condiciones de pertenencia
            #mud.send_message(id, f"Debug: target_name in players_here: {target_name in players_here}")
            #mud.send_message(id, f"Debug: target_name not in players_here: {target_name not in players_here}")

            # Verificar si el objetivo está en la lista de jugadores en la sala
            if target_name in players_here:
                # Encontrar el ID del jugador objetivo
                victima_id = next(pid for pid, pl in players.items() 
                                  if pl["name"].strip().lower() == target_name 
                                  and players[pid]["room"] == players[id]["room"])
                iniciar_combate(players, id, players[victima_id]["name"], mud)
            else:
                mud.send_message(id, f"No se encontró al jugador '{params.strip()}'.")

        else:
            # Comprobar si el comando es una salida válida en la sala actual
            try:
                room = load_room(players[id]["room"])
                if command in room["exits"]:
                    move_player(id, command)
                else:
                    mud.send_message(id, f"No conozco la orden '{command}' (escribe: ayuda para ver los comandos disponibles)")
            except ValueError as e:
                print(f"[ERR] Error loading room (pid= {id}): {e}")  # Debug por salida estándar
                mud.send_message(id, "\033[31mHas sufrido un fallo espacio/tiempo y apareces en la incubadora.\033[0m")
                players[id]["room"] = "respawn"
                mostrar_sala_al_jugador(id)
    # Procesar turnos de combate
    procesar_turno_combate(players, mud, mostrar_sala_al_jugador)
