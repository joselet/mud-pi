#!/usr/bin/env python

import time
import os
import json  # Puedes usar `yaml` si prefieres archivos YAML
from mudserver import MudServer

# Carpeta donde están almacenadas las salas
ROOMS_DIR = "rooms"

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
    with open(room_file, "r") as file:
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
            for pid, pl in players.items():
                if players[pid]["room"] == players[id]["room"] and pid != id:
                    mud.send_message(pid, f"{players[id]['name']} left via exit '{ex}'")
            
            players[id]["room"] = room["exits"][ex]
            new_room = load_room(players[id]["room"])
            for pid, pl in players.items():
                if players[pid]["room"] == players[id]["room"] and pid != id:
                    mud.send_message(pid, f"{players[id]['name']} arrived via exit '{ex}'")
            
            mud.send_message(id, f"You arrive at '{players[id]['room']}'")
            mud.send_message(id, new_room["title"])
            mud.send_message(id, new_room["description"])
            # Mostrar jugadores presentes en la nueva sala (excluyendo al jugador actual)
            players_here = [pl["name"] for pid, pl in players.items() if players[pid]["room"] == players[id]["room"] and pid != id]
            if players_here:
                mud.send_message(id, f"Players here: {', '.join(players_here)}")
            else:
                mud.send_message(id, "You are alone here.")
            mud.send_message(id, f"Exits are: {', '.join(new_room['exits'])}")
        else:
            mud.send_message(id, f"Unknown exit '{ex}'")
    except ValueError as e:
        mud.send_message(id, f"Error loading room: {e}")

# Stores the players in the game
players = {}

# Start the server
mud = MudServer()

# Main game loop
while True:
    time.sleep(0.2)
    mud.update()

    for id in mud.get_new_players():
        players[id] = {"name": None, "room": None}
        mud.send_message(id, "What is your name?")

    for id in mud.get_disconnected_players():
        if id not in players:
            continue
        for pid, pl in players.items():
            mud.send_message(pid, f"{players[id]['name']} quit the game")
        del players[id]

    for id, command, params in mud.get_commands():
        if id not in players:
            continue

        if players[id]["name"] is None:
            players[id]["name"] = command
            players[id]["room"] = "Tavern"
            mud.send_message(id, f"Welcome to the game, {players[id]['name']}. Type 'help' for a list of commands. Have fun!")
            try:
                room = load_room(players[id]["room"])
                mud.send_message(id, room["description"])
            except ValueError as e:
                mud.send_message(id, f"Error loading room: {e}")

        elif command == "help":
            mud.send_message(id, "Commands:")
            mud.send_message(id, "  say <message>  - Says something out loud, e.g. 'say Hello'")
            mud.send_message(id, "  look           - Examines the surroundings, e.g. 'look'")
            mud.send_message(id, "  go <exit>      - Moves through the exit specified, e.g. 'go outside'")
            mud.send_message(id, "  <exit>         - Shortcut to move through an exit, e.g. 'outside'")
            mud.send_message(id, "  salir          - Abandonar el juego")
        elif command == "say":
            for pid, pl in players.items():
                if players[pid]["room"] == players[id]["room"]:
                    mud.send_message(pid, f"{players[id]['name']} says: {params}")

        elif command == "look":
            try:
                room = load_room(players[id]["room"])
                mud.send_message(id, room["description"])
                # Mostrar jugadores presentes en la nueva sala (excluyendo al jugador actual)
                players_here = [pl["name"] for pid, pl in players.items() if players[pid]["room"] == players[id]["room"] and pid != id]
                if players_here:
                    mud.send_message(id, f"Players here: {', '.join(players_here)}")
                else:
                    mud.send_message(id, "You are alone here.")
                mud.send_message(id, f"Exits are: {', '.join(room['exits'])}")
            except ValueError as e:
                mud.send_message(id, f"Error loading room: {e}")

        elif command == "go":
            move_player(id, params)
        elif command == "salir":
            mud.send_message(id, "Disconnecting. Goodbye!")
            mud._handle_disconnect(id)
            if id in players:
                del players[id]
        else:
            # Comprobar si el comando es una salida válida en la sala actual
            try:
                room = load_room(players[id]["room"])
                if command in room["exits"]:
                    move_player(id, command)
                else:
                    mud.send_message(id, f"Unknown command '{command}'")
            except ValueError as e:
                mud.send_message(id, f"Error loading room: {e}")
