#!/usr/bin/env python

import time
import sqlite3
import random
from mudserver import MudServer
from sistema_de_combate import iniciar_combate, procesar_turno_combate

# Carpeta donde están almacenadas las salas
ROOMS_DIR = "rooms"
# Carpeta donde se almacenan las fichas de los jugadores
PLAYERS_DIR = "players"
DB_PATH = "data/mud.db"

#descripcion de los niveles: infrarojo, rojo, naranja, amarillo, verde, indigo, morado, ultravioleta, x
NIVEL_DISPLAY = {
    0: "IR",
    1: "R",
    2: "N",
    3: "Y",
    4: "V",
    5: "I",
    6: "M",
    7: "UV",
    8: "X"
}
# Cache para las salas cargadas
rooms_cache = {}

# Función para cargar una sala desde un archivo
def load_room(room_name):
    # Si la sala ya está en la caché, devolverla
    if room_name in rooms_cache:
        return rooms_cache[room_name]

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Buscar la sala por nombre
    cur.execute("SELECT * FROM rooms WHERE name = ?", (room_name.lower(),))
    room_row = cur.fetchone()
    if not room_row:
        conn.close()
        raise ValueError(f"Room not found in DB: {room_name}")

    # Buscar las salidas de la sala
    cur.execute("SELECT exit_name, target_room FROM exits WHERE room_name = ?", (room_name.lower(),))
    exits = {row["exit_name"]: row["target_room"] for row in cur.fetchall()}

    room_data = {
        "title": room_row["title"],
        "description": room_row["description"],
        "exits": exits
    }

    conn.close()

    # Verificar que la sala tiene los campos obligatorios
    required_keys = {"title", "description", "exits"}
    if not required_keys.issubset(room_data.keys()):
        raise ValueError(f"Room '{room_name}' is missing required keys: {required_keys - room_data.keys()}")

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
                    mud.send_message(pid, f"{players[id]['display_name']} se fue hacia '{ex}'")
            
            # Mover al jugador
            players[id]["room"] = room["exits"][ex]
            new_room = players[id]["room"]  # Store the new room after moving
            
            # Determinar la salida que lleva al current_room desde la nueva sala
            reverse_exit = next((exit_name for exit_name, target_room in load_room(new_room)["exits"].items() if target_room == current_room), "algún lugar desconocido")
            
            # Notificar llegada al resto de jugadores en la nueva sala
            for pid, pl in players.items():
                if players[pid]["room"] == new_room and pid != id:
                    mud.send_message(pid, f"{players[id]['display_name']} llega desde '{reverse_exit}'")
            
            # Mostrar la sala al jugador usando la función ya existente
            mostrar_sala_al_jugador(id)
        else:
            mud.send_message(id, f"Salida desconocida '{ex}'")
    except ValueError as e:
        print(f"[ERR] Error loading room (pid= {id}): {e}")  # Debug por salida estándar
        mud.send_message(id, "\033[31mHas sufrido un fallo espacio/tiempo y apareces en la incubadora.\033[0m")
        players[id]["room"] = "respawn"
        mostrar_sala_al_jugador(id)

def cargar_jugador(nombre):
    """Carga un jugador existente desde la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM players WHERE name = ?", (nombre.lower(),))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise ValueError("Jugador no encontrado.")
    ficha = dict(row)
    ficha["display_name"] = f"{ficha['name'].capitalize()}-{ficha['sector']}-{ficha['clon']}"
    return ficha

def crear_jugador(nombre, password):
    """Crea un nuevo jugador y lo guarda en la base de datos."""
    ficha = {
        "name": nombre,
        "password": password,
        "nivel": 0,
        "clon": 1,
        "pv": 100,
        "e": 100,
        "f": random.randint(1, 20),
        "r": random.randint(1, 20),
        "a": random.randint(1, 20),
        "d": random.randint(1, 20),
        "p": random.randint(1, 20),
        "c": random.randint(1, 20),
        "tm": random.randint(1, 20),
        "pm": random.randint(1, 20),
        "servicio": None,
        "sociedad_secreta": None,
        "sector": None,
        "room": "inicio"
    }
    # Servicio
    servicio_roll = random.randint(1, 20)
    if servicio_roll <= 2:
        ficha["servicio"] = "SSI"
    elif servicio_roll <= 4:
        ficha["servicio"] = "STC"
    elif servicio_roll <= 8:
        ficha["servicio"] = "SBD"
    elif servicio_roll <= 11:
        ficha["servicio"] = "SDF"
    elif servicio_roll <= 14:
        ficha["servicio"] = "SPL"
    elif servicio_roll <= 16:
        ficha["servicio"] = "SEG"
    elif servicio_roll <= 18:
        ficha["servicio"] = "SID"
    else:
        ficha["servicio"] = "SCP"
    # Sociedad secreta
    sociedad_roll = random.randint(1, 10)
    if sociedad_roll <= 2:
        ficha["sociedad_secreta"] = "Antimutantes"
    elif sociedad_roll <= 4:
        ficha["sociedad_secreta"] = "Piratas Informáticos"
    elif sociedad_roll <= 7:
        ficha["sociedad_secreta"] = "Comunistas"
    else:
        ficha["sociedad_secreta"] = "Iglesia Primitiva del Cristo Programador"
    # Sector
    sector_roll = random.randint(1, 10)
    if sector_roll <= 2:
        ficha["sector"] = "OTE"
    elif sector_roll <= 4:
        ficha["sector"] = "EKO"
    elif sector_roll <= 7:
        ficha["sector"] = "ANO"
    else:
        ficha["sector"] = "ICO"

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO players (name, password, nivel, clon, pv, e, f, r, a, d, p, c, tm, pm, servicio, sociedad_secreta, sector, room)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ficha["name"], ficha["password"], ficha["nivel"], ficha["clon"], ficha["pv"], ficha["e"], ficha["f"], ficha["r"], ficha["a"],
        ficha["d"], ficha["p"], ficha["c"], ficha["tm"], ficha["pm"], ficha["servicio"],
        ficha["sociedad_secreta"], ficha["sector"], ficha["room"]
    ))
    conn.commit()
    conn.close()

    ficha["display_name"] = f"{ficha['name'].capitalize()}-{ficha['sector']}-{ficha['clon']}"
    return ficha

def guardar_jugador(ficha):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        UPDATE players SET
            nivel = ?, clon = ?, pv = ?, e = ?, f = ?, r = ?, a = ?, d = ?, p = ?, c = ?, tm = ?, pm = ?,
            servicio = ?, sociedad_secreta = ?, sector = ?, room = ?
        WHERE name = ?
    """, (
        ficha.get("nivel", 0), ficha.get("clon", 1), ficha["pv"], ficha["e"], ficha["f"], ficha["r"], ficha["a"], ficha["d"],
        ficha["p"], ficha["c"], ficha["tm"], ficha["pm"], ficha["servicio"], ficha["sociedad_secreta"], ficha.get("sector", None), ficha["room"], ficha["name"]
    ))
    conn.commit()
    conn.close()

def mostrar_sala_al_jugador(id):
    try:
        room = load_room(players[id]["room"])
        mud.send_message(id, room["title"])
        mud.send_message(id, room["description"])
        print(f"[LOG] (pid= {id}): {room["title"]}")  # Debug por salida estándar
        # Mostrar jugadores presentes en la nueva sala (excluyendo al jugador actual)
        players_here = [pl["display_name"] for pid, pl in players.items() if players[pid]["room"] == players[id]["room"] and pid != id]
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

# Diccionario de alias para las salidas típicas
EXIT_ALIASES = {
    "n": "norte",
    "s": "sur",
    "e": "este",
    "o": "oeste",
    "ne": "noreste",
    "no": "noroeste",
    "se": "sudeste",
    "so": "sudoeste",
    "ar": "arriba",
    "ab": "abajo",
    "de": "dentro",
    "fu": "fuera"
}

def validar_contraseña(nombre, password):
    """Valida la contraseña de un jugador existente."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT password FROM players WHERE name = ?", (nombre.lower(),))
    row = cur.fetchone()
    conn.close()
    if row and row["password"] == password:
        return True
    elif row:
        raise ValueError("Contraseña incorrecta.")
    return False

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
        # Guardar la sala actual en la base de datos antes de eliminar al jugador
        ficha = players[id]
        ficha["room"] = players[id]["room"]
        guardar_jugador(ficha)
        # Notificar a todos los jugadores que alguien ha salido
        for pid, pl in players.items():
            if pid != id:
                mud.send_message(pid, f"{players[id]['display_name']} salió del juego.")
        del players[id]

    for id, command, params in mud.get_commands():
        if id not in players:
            continue

        # Verificar si el comando es un alias de salida
        if command in EXIT_ALIASES:
            command = EXIT_ALIASES[command]  # Traducir alias al nombre completo

        if players[id]["awaiting_name"]:
            # Handle name input
            player_name = command.strip()
            players[id]["name"] = player_name
            players[id]["awaiting_name"] = False
            players[id]["awaiting_password"] = True
            players[id]["password_attempts"] = 0  # Initialize password attempts
            # Comprobar si el jugador existe en la base de datos
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM players WHERE name = ?", (player_name.lower(),))
            exists = cur.fetchone()
            conn.close()
            if exists:
                mud.send_message(id, "Personaje encontrado. Dame la contraseña:")
            else:
                mud.send_message(id, "Personaje no encontrado. Vamos a crearlo. Por favor, establece una contraseña:")
                players[id]["crear_jugador"] = True
        elif players[id].get("awaiting_password"):
            # Step 2: Handle password input with retry mechanism
            try:
                password = command.strip()
                if players[id].get("crear_jugador"):
                    # Crear un nuevo jugador
                    ficha = crear_jugador(players[id]["name"], password)
                else:
                    # Validar la contraseña y cargar el jugador existente
                    if not validar_contraseña(players[id]["name"], password):
                        raise ValueError("Contraseña incorrecta.")
                    ficha = cargar_jugador(players[id]["name"])

                # Verificar si el jugador ya está conectado
                for pid, pl in players.items():
                    if pid != id and pl["name"] == players[id]["name"]:
                        guardar_jugador(players[pid])
                        mud.send_message(pid, "\033[31mEl ordenador ha detectado una suplantación de identidad...\033[0m")
                        mud._handle_disconnect(pid)
                        del players[pid]
                        break

                # Actualizar el estado del jugador
                players[id].update(ficha)
                players[id]["awaiting_password"] = False
                mud.send_message(id, f"Bienvenido al juego, {players[id]['display_name']}. Escribe 'ayuda' para obtener una lista de comandos.")
                mostrar_sala_al_jugador(id)
                # Notificar a otros jugadores
                for pid, pl in players.items():
                    if pid != id:
                        mud.send_message(pid, f"[info] {players[id]['display_name']} entró al juego.")
                # Notificar a los jugadores de la sala actual que alguien acaba de aparecer
                for pid, pl in players.items():
                    if players[pid]["room"] == players[id]["room"] and pid != id:
                        mud.send_message(pid, f"{players[id]['display_name']} acaba de aparecer en la sala por arte de magia.")
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
            mud.send_message(id, "  estado         - Comprobar la ficha y estado de tu personaje")
            mud.send_message(id, "  matar <objetivo> - Atacar a otro personaje")
            mud.send_message(id, "  abandonar          - Abandonar el juego")

        elif command == "decir":
            for pid, pl in players.items():
                if players[pid]["room"] == players[id]["room"]:
                    mud.send_message(pid, f"{players[id]['display_name']} dice: {params}")

        elif command == "mirar":
            mostrar_sala_al_jugador(id)

        elif command == "ir":
            move_player(id, params)

        elif command == "abandonar":
            mud.send_message(id, "Desconectando. Adiós!")
            # Guardar la sala actual en la base de datos antes de eliminar al jugador
            ficha = players[id]
            ficha["room"] = players[id]["room"]
            guardar_jugador(ficha)
            # Notificar al resto de jugadores que alguien ha salido
            for pid, pl in players.items():
                if pid != id:
                    mud.send_message(pid, f"[info] {players[id]['name']} se marchó del juego.")
            print(f"[LOG] {players[id]['name']} salió del juego (id={id})")
            mud._handle_disconnect(id)
            if id in players:
                del players[id]

        elif command == "estado":
            ficha = players[id]
            mud.send_message(id, (
                f"Eres {ficha['display_name']}, agente esclarecedor con Código de Seguridad: {NIVEL_DISPLAY.get(ficha.get('nivel', 0))} y clonado {ficha.get('clon', 1)} veces:\n"
                f"Te han asignado al servicio: {ficha.get('servicio', 'Ninguno')}\n"
                f"Perteneces a la sociedad secreta: {ficha.get('sociedad_secreta', 'Ninguna')}\n"
                f"Vives en el sector: {ficha.get('sector', 'Desconocido')}\n"
                f"  Vida (pv): {ficha.get('pv', 0)}\n"
                f"  Energía (e): {ficha.get('e', 0)}\n"
                f"  Fuerza (f): {ficha.get('f', 0)}\n"
                f"  Resistencia (r): {ficha.get('r', 0)}\n"
                f"  Agilidad (a): {ficha.get('a', 0)}\n"
                f"  Destreza (d): {ficha.get('d', 0)}\n"
                f"  Percepcion (p): {ficha.get('p', 0)}\n"
                f"  Cinismo (c): {ficha.get('c', 0)}\n"
                f"  Talento mecánico (tm): {ficha.get('tm', 0)}\n"
                f"  Poder mutante (pm): {ficha.get('pm', 0)}\n"
                f"  Sala actual: {ficha.get('room', 'Desconocida')}"
            ))

        elif command == "matar":
            # Iniciar combate usando la función de sistema_de_combate
            iniciar_combate(players, id, params, mud)

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


