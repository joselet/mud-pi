-- Tabla de habitaciones
CREATE TABLE IF NOT EXISTS rooms (
    name TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL
);

-- Tabla de salidas
CREATE TABLE IF NOT EXISTS exits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_name TEXT NOT NULL,
    exit_name TEXT NOT NULL,
    target_room TEXT NOT NULL,
    FOREIGN KEY(room_name) REFERENCES rooms(name),
    FOREIGN KEY(target_room) REFERENCES rooms(name)
);