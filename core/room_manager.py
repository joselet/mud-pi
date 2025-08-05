import sqlite3
from .config import REVERSED_COMMAND_ALIASES, adaptaTexto  # Import the reversed aliases and adaptaTexto

class RoomManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.rooms_cache = {}

    def players_in_room(self, room_name, players):
        """
        Devuelve una lista de IDs de jugadores presentes en una sala específica.
        """
        return [pid for pid, pl in players.items() if pl["room"] == room_name]

    def load_room(self, room_name):
        # Si la sala ya está en la caché, devolverla
        if room_name in self.rooms_cache:
            return self.rooms_cache[room_name]

        conn = sqlite3.connect(self.db_path)
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

        # Buscar los objetos de la sala
        cur.execute("SELECT object_name, description FROM room_objects WHERE room_name = ?", (room_name.lower(),))
        objects = {}
        for row in cur.fetchall():
            # Dividir object_name en una lista de alias
            aliases = row["object_name"].split(",")
            for alias in aliases:
                alias = alias.strip().lower()  # Normalizar los alias
                objects[alias] = {
                    "description": row["description"],
                    "interactions": {}  # Aquí almacenaremos los comandos y efectos
                }

        # Buscar las interacciones de los objetos en la sala
        cur.execute("SELECT object_name, command, effect, message, cooldown, cooldown_message FROM object_interactions WHERE room_name = ?", (room_name.lower(),))
        interactions = {}
        for row in cur.fetchall():
            key = f"{row['command']} {row['object_name']}".lower()
            interactions[key] = {
                "effect": row["effect"],
                "message": row["message"],
                "cooldown": row["cooldown"] or 0,  # Usa 0 si cooldown es None
                "cooldown_message": row["cooldown_message"]
            }

        room_data = {
            "name": room_row["name"],
            "title": room_row["title"],
            "description": room_row["description"],
            "exits": exits,
            "objects": objects,  # Incluye los objetos con sus interacciones
            "interactions": interactions  # Agregar las interacciones a los datos de la sala
        }

        conn.close()

        # Verificar que la sala tiene los campos obligatorios
        required_keys = {"title", "description", "exits"}
        if not required_keys.issubset(room_data.keys()):
            raise ValueError(f"Room '{room_name}' is missing required keys: {required_keys - room_data.keys()}")

        # Almacenar en la caché y devolver
        self.rooms_cache[room_name] = room_data
        return room_data

    def show_room_to_player(self, id, players, mud):
        try:
            room = self.load_room(players[id]["room"])
            if players[id]["config"].get("detallado", True):  # Default to detailed view if not set
                mud.send_message(id, room["title"])
                mud.send_message(id, room["description"].replace("\\n", "\n"))
                print(f"[LOG] (pid= {id}): {room['name']}: {room['title']}")  # Debug output
            else:  # Simplified mode
                # Convert full exit names to aliases using REVERSED_COMMAND_ALIASES
                exit_aliases = [REVERSED_COMMAND_ALIASES.get(exit_name, exit_name) for exit_name in room["exits"].keys()]
                mud.send_message(id, f"{room['title']} [{','.join(exit_aliases)}]")
            
            # Mostrar jugadores en la sala
            players_here = [pl["display_name"] for pid, pl in players.items() if players[pid]["room"] == players[id]["room"] and pid != id]
            if players_here:
                mud.send_message(id, f"Aquí ves a: {', '.join(players_here)}")
            else:
                mud.send_message(id, "Estás solo aquí.")
    
            # Mostrar NPCs en la sala
            npcs = self.load_npcs_in_room(players[id]["room"])
            if npcs:
                npc_names = [npc["display_name"] for npc in npcs]
                mud.send_message(id, f"Aquí ves a los siguientes NPCs: {', '.join(npc_names)}")

            # Show exits (detailed view)
            if players[id]["config"].get("detallado", True):
                mud.send_message(id, f"Salidas: {', '.join(room['exits'])}")
        except ValueError as e:
            print(f"[ERR] Error loading room (pid= {id}): {e}")  # Debug output
            mud.send_message(id, "\033[31mHas sufrido un fallo espacio/tiempo y apareces en la incubadora.\033[0m")
            players[id]["room"] = "respawn"
            self.show_room_to_player(id, players, mud)

    def move_player(self, id, exit_name, players, mud):
        try:
            room = self.load_room(players[id]["room"])
            ex = exit_name.lower()
            if ex in room["exits"]:
                current_room = players[id]["room"]  # Store the current room before moving
                # Notify players in the current room about the player's exit
                for pid, pl in players.items():
                    if players[pid]["room"] == current_room and pid != id:
                        mud.send_message(pid, f"{players[id]['display_name']} se fue hacia '{ex}'")
                
                # Move the player
                players[id]["room"] = room["exits"][ex]
                new_room = players[id]["room"]  # Store the new room after moving
                
                # Determine the reverse exit leading back to the current room
                reverse_exit = next((exit_name for exit_name, target_room in self.load_room(new_room)["exits"].items() if target_room == current_room), "algún lugar desconocido")
                
                # Notify players in the new room about the player's arrival
                for pid, pl in players.items():
                    if players[pid]["room"] == new_room and pid != id:
                        mud.send_message(pid, f"{players[id]['display_name']} llega desde '{reverse_exit}'")
                
                # Show the new room to the player
                self.show_room_to_player(id, players, mud)
            else:
                mud.send_message(id, f"Salida desconocida '{ex}'")
        except ValueError as e:
            print(f"[ERR] Error loading room (pid= {id}): {e}")  # Debug output
            mud.send_message(id, "\033[31mHas sufrido un fallo espacio/tiempo y apareces en la incubadora.\033[0m")
            players[id]["room"] = "respawn"
            self.show_room_to_player(id, players, mud)


    def load_npcs_in_room(self, room_name):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM npcs WHERE room = ? AND pv > 0", (room_name,))  # Filtrar NPCs con pv > 0
        npcs = [dict(row) for row in cur.fetchall()]
        # asignar un id a cada NPC
        for i, npc in enumerate(npcs):
            npc["id"] = f"_npc{npc['id']}"
            npc["description"] = adaptaTexto(npc["description"])
        conn.close()
        return npcs

    def save_npc(self, npc):
        npc_bd_id = npc["id"].replace("_npc", "")
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        # Actualizar el NPC en la base de datos
        cur.execute("""
            UPDATE npcs SET pv = ?, room = ?
            WHERE id = ?
        """,(npc["pv"], npc["room"], npc_bd_id))
        conn.commit()
        conn.close()
