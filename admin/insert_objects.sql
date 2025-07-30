drop table if exists room_objects;
CREATE TABLE room_objects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_name TEXT NOT NULL,
    object_name TEXT NOT NULL,
    description TEXT NOT NULL
);

-- Ejemplo de inserción de objetos
INSERT INTO room_objects (room_name, object_name, description) VALUES
('lab/p3_pasillo_genetico', 'fuente', 'Una fuente de la que brota un montón de bebida espumosa.'),
('lab/p3_pasillo_genetico', 'camilla', 'Una camilla de hospital con un cuerpo inerte cubierto por una sábana con manchas de sangre. Dudas si quieres ´destapar camilla´ Te aterroriza ver lo que oculta la sábana.'),
('lab/camara_criogenica', 'armario', 'Un armario metálico con puertas cerradas herméticamente. En una de las puertas ves una pegatina advirtiendo de un posible peligro.');

drop table if exists object_interactions;
CREATE TABLE object_interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    object_name TEXT NOT NULL,
    room_name TEXT NOT NULL,
    command TEXT NOT NULL, -- Comando asociado (como "beber", "abrir")
    effect TEXT,           -- Efecto del comando (como "energia+5")
    message TEXT           -- Mensaje al ejecutar el comando (opcional)
);

-- Ejemplo de inserción de interacciones
INSERT INTO object_interactions (object_name, room_name, command, effect, message) VALUES
('fuente', 'lab/p3_pasillo_genetico', 'beber', 'energia+5', 'Recuperas un poco de energía.'),
('fuente', 'lab/p3_pasillo_genetico', 'romper', NULL, 'Desistes en tu intento de estropear la fuente'),
('camilla', 'lab/p3_pasillo_genetico', 'destapar', NULL, 'Aterrorizado, caes al suelo'),
('armario', 'lab/camara_criogenica', 'abrir', NULL, 'El armario está cerrado con llave.');