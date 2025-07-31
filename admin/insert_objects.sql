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
('lab/p3_pasillo_genetico', 'camilla,camillas,cuerpo,cuerpos', 'Varias camillas de hospital con cuerpos inertes cubiertos por una sábana, algunas con manchas de sangre. Dudas si quieres ´destapar camilla´ Te aterroriza ver lo que oculta la sábana.'),
('lab/camara_criogenica', 'armario', 'Un armario metálico con puertas cerradas herméticamente. En una de las puertas ves una pegatina advirtiendo de un posible peligro.');

drop table if exists object_interactions;
CREATE TABLE object_interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    object_name TEXT NOT NULL,
    room_name TEXT NOT NULL,
    command TEXT NOT NULL,       -- Comando asociado (como "beber", "abrir")
    effect TEXT,
    message TEXT,                 -- Mensaje al ejecutar el comando (opcional)
    cooldown INTEGER,  -- Tiempo de reutilización del comando (en segundos)
    cooldown_message TEXT DEFAULT 'Por algun motivo no puedes hacer eso ahora. Quizá esperando un poco...' -- Mensaje de cooldown
);

-- Ejemplo de inserción de interacciones
INSERT INTO object_interactions (object_name, room_name, command, effect, message, cooldown, cooldown_message) VALUES
('fuente', 'lab/p3_pasillo_genetico', 'beber', 'energia+5', 'La fuente burbujea suavemente mientras bebes de ella. Sientes un ligero cosquilleo en tu cuerpo.', 30, 'Bebes de la fuente, te notas algo empachad@. (vuelve a beber en % segundos)'),
('fuente', 'lab/p3_pasillo_genetico', 'romper', NULL, 'Desistes en tu intento de estropear la fuente', 0, NULL),
('camilla', 'lab/p3_pasillo_genetico', 'destapar', NULL, 'Aterrorizad@, caes al suelo', 10, 'Por experiencia, no deseas presenciar lo que hace un momento se ha visto bajo la sábana'),
('armario', 'lab/camara_criogenica', 'abrir', NULL, 'El armario está cerrado con llave.', NULL, NULL);