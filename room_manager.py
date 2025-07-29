import sqlite3

class RoomManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.rooms_cache = {}

    def load_room(self, room_name):
        # ...existing code for loading a room...
        pass

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
