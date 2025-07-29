#!/usr/bin/env python

from mud_game import MudGame

DB_PATH = "data/mud.db"

if __name__ == "__main__":
    game = MudGame(DB_PATH)
    game.run()

"""
import time
import sqlite3
import random
from mudserver import MudServer

DB_PATH = "data/mud.db"

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


# https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
# https://en.wikipedia.org/wiki/ANSI_escape_code
NIVEL_COLOR = {
    0: "\033[37m",  # IR (37)
    1: "\033[91m",  # R
    2: "\033[33m",  # N
    3: "\033[93m",  # Y
    4: "\033[92m",  # V
    5: "\033[96m",  # I (o 94)
    6: "\033[95m",  # M
    7: "\033[35m",  # UV
    8: "\033[97m",   # X
    "reset": "\033[0m"  # Reset color
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
    # Carga un jugador existente desde la base de datos.
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
    # Crea un nuevo jugador y lo guarda en la base de datos.
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
    cur.execute("
        INSERT INTO players (name, password, nivel, clon, pv, e, f, r, a, d, p, c, tm, pm, servicio, sociedad_secreta, sector, room)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ", (
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
    cur.execute("
        UPDATE players SET
            nivel = ?, clon = ?, pv = ?, e = ?, f = ?, r = ?, a = ?, d = ?, p = ?, c = ?, tm = ?, pm = ?,
            servicio = ?, sociedad_secreta = ?, sector = ?, room = ?
        WHERE name = ?
    ", (
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


def validar_contraseña(nombre, password):
    # Valida la contraseña de un jugador existente.
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



# sistema de combate
combates_activos = {}

def iniciar_combate(players, atacante_id, victima_nombre, mud):
    # Procesar el nombre de la víctima para garantizar consistencia
    victima_nombre = victima_nombre.strip().lower()

    # Buscar el ID de la víctima de manera consistente
    victima_id = None
    for pid, pl in players.items():
        if pl["name"].strip().lower() == victima_nombre and players[pid]["room"] == players[atacante_id]["room"]:
            victima_id = pid
            break

    # Verificar si no se encontró un ID válido
    if victima_id is None:
        mud.send_message(atacante_id, f"No se encontró al jugador '{victima_nombre}' en esta sala.")
        return

    # Registrar el combate si no está ya activo
    if atacante_id in combates_activos or victima_id in combates_activos:
        mud.send_message(atacante_id, "Ya estás en un combate.")
        return

    combates_activos[atacante_id] = {"victima": victima_id, "turno": atacante_id}
    combates_activos[victima_id] = {"victima": atacante_id, "turno": atacante_id}

    # Notificar a los jugadores
    mud.send_message(atacante_id, f"Has iniciado un combate contra {players[victima_id]['display_name']}.")
    mud.send_message(victima_id, f"{players[atacante_id]['display_name']} te ha atacado. ¡Prepárate para luchar!")

def procesar_turno_combate(players, mud):
    for atacante_id, combate in list(combates_activos.items()):
        # Solo procesar el turno del atacante actual
        if combate["turno"] != atacante_id:
            continue

        victima_id = combate["victima"]
        atacante = players[atacante_id]
        victima = players[victima_id]

        # Verificar si ambos jugadores están en la misma sala
        if atacante["room"] != victima["room"]:
            # una propuesta para que el combate sea persistente si vuelven a encontrarse los implicados es que
            # este if solo comprueba si es la misma rooom con un == no se envian textos de que ha rerminado el combate ni se eliminan los combates
            # y el resto del codigo iría dentro del if
            mud.send_message(atacante_id, f"El combate con {victima['display_name']} ha terminado porque ya no están en la misma sala.")
            mud.send_message(victima_id, f"El combate con {atacante['display_name']} ha terminado porque ya no están en la misma sala.")
            del combates_activos[atacante_id]
            del combates_activos[victima_id]
            continue

        # Verificar si el atacante tiene suficiente energía
        if atacante["e"] <= 0:
            mud.send_message(atacante_id, "No tienes suficiente energía para atacar.")
            mud.send_message(victima_id, f"{atacante['display_name']} Realiza un penoso gesto de ataque, pero agotado desfallece en el intento.")
            combate["turno"] = victima_id  # Pasar el turno a la víctima
        else:
            # Calcular daño
            tirada = random.randint(0, 5)
            dano = max(0, atacante["f"] + tirada - victima["d"])
            victima["pv"] -= dano
            atacante["e"] -= 1  # Restar energía al atacante

            # Notificar a los jugadores
            mud.send_message(atacante_id, f"Tirada: {atacante['f']} (Fue.A) + {tirada} - {victima['d']} (Des.D) = {dano} -> Has infligido {dano} de daño a {victima['display_name']}.")
            mud.send_message(victima_id, f"Tirada: {atacante['f']} (Fue.A) + {tirada} - {victima['d']} (Des.D) = {dano} -> Has recibido {dano} de daño de {atacante['display_name']}. Puntos de vida restantes: {victima['pv']}")

            # Verificar si la víctima ha muerto
            if victima["pv"] <= 0:
                finalizar_combate(atacante_id, victima_id, players, mud, mostrar_sala_al_jugador)
                continue

        # Pasar el turno a la víctima
        combate["turno"] = victima_id

        # Respuesta automática de la víctima
        if victima["e"] > 0:
            respuesta_tirada = random.randint(0, 5)
            respuesta_dano = max(0, victima["f"] + respuesta_tirada - atacante["d"])
            atacante["pv"] -= respuesta_dano
            victima["e"] -= 1  # Restar energía a la víctima

            # Notificar a los jugadores
            mud.send_message(victima_id, f"Tirada: {victima['f']} (Fue.V) + {respuesta_tirada} - {atacante['d']} (Des.A) = {respuesta_dano} -> En respuesta, Has infligido {respuesta_dano} de daño a {atacante['display_name']}.")
            mud.send_message(atacante_id, f"Tirada: {victima['f']} (Fue.V) + {respuesta_tirada} - {atacante['d']} (Des.A) = {respuesta_dano} -> En respuesta, Has recibido {respuesta_dano} de daño de {victima['display_name']}. Puntos de vida restantes: {atacante['pv']}")

            # Verificar si el atacante ha muerto
            if atacante["pv"] <= 0:
                finalizar_combate(victima_id, atacante_id, players, mud, mostrar_sala_al_jugador)
                continue
        else:
            mud.send_message(victima_id, "No tienes suficiente energía para contraatacar.")
            mud.send_message(atacante_id, f"{victima['display_name']} Realiza un penoso gesto de ataque, pero agotado desfallece en el intento.")

        # Si ninguno muere, devolver el turno al atacante
        combate["turno"] = atacante_id

def finalizar_combate(ganador_id, perdedor_id, players, mud, mostrar_sala_al_jugador):
    # Finaliza el combate entre los jugadores
    del combates_activos[ganador_id]
    del combates_activos[perdedor_id]

    # Notificar al ganador y al perdedor
    mud.send_message(ganador_id, f"\033[93m¡Has derrotado a {players[perdedor_id]['display_name']}!\033[0m")
    mud.send_message(perdedor_id, f"\033[31m¡Has sido derrotado por {players[ganador_id]['display_name']}!\033[0m")
    mud.send_message(perdedor_id, "\033[93mDebido a tu pobre genética, las celulas de tu cuerpo se deshacen lentamente debido a la falta de irrigación mantenida por tu bomba de fluido sanguíneo.\nPor imperativa del ordenador, los restos de tu triste cuerpo son trasladados a la planta de regeneración para ser reciclados y finalmene formar una nueva vida.\nTu alma y tu psique es transferida a un nuevo cuerpo.\033[0m")

    # Notificar a todos los jugadores que alguien ha muerto
    for pid, pl in players.items():
        if pid != perdedor_id:
            mud.send_message(pid, f"[info] {players[perdedor_id]['name']} ha muerto.")

    # Enviar al perdedor a la sala de incubadora
    players[perdedor_id]["room"] = "respawn"
    mostrar_sala_al_jugador(perdedor_id)

    # Incrementar el clon del perdedor
    players[perdedor_id]["clon"] += 1
    players[perdedor_id]["display_name"] = f"{players[perdedor_id]['name'].capitalize()}-{players[perdedor_id]['sector']}-{players[perdedor_id]['clon']}"

    # Restablecer un porcentaje de la vida del perdedor
    players[perdedor_id]["pv"] = 25
"""


