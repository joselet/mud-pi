import sqlite3

class RoomManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.rooms_cache = {}

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
        cur.execute("SELECT object_name, description, interaction_command, interaction_effect, interaction_message FROM room_objects WHERE room_name = ?", (room_name.lower(),))
        objects = {row["object_name"]: {"description": row["description"], "interaction_command": row["interaction_command"], "interaction_effect": row["interaction_effect"], "interaction_message": row["interaction_message"]} for row in cur.fetchall()}

        room_data = {
            "title": room_row["title"],
            "description": room_row["description"],
            "exits": exits,
            "objects": objects  
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
            mud.send_message(id, room["title"])
            mud.send_message(id, room["description"])
            print(f"[LOG] (pid= {id}): {room['title']}")  # Debug output
            # Show other players in the room
            players_here = [pl["display_name"] for pid, pl in players.items() if players[pid]["room"] == players[id]["room"] and pid != id]
            if players_here:
                mud.send_message(id, f"Aquí ves a: {', '.join(players_here)}")
            else:
                mud.send_message(id, "Estás solo aquí.")
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
