import sqlite3

class RoomManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.rooms_cache = {}

    def load_room(self, room_name):
        # ...existing code for loading a room...
