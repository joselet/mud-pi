drop table if exists room_objects;
CREATE TABLE room_objects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_name TEXT NOT NULL,
    object_name TEXT NOT NULL,
    description TEXT NOT NULL
);

-- Ejemplo de inserción de objetos
INSERT INTO room_objects (room_name, object_name, description) VALUES
('inicio', 'probeta', 'Una probeta de cristal llena de un líquido azulado semi-transparente. Parece que contiene algún tipo de sustancia química.'),
('inicio', 'tubo,tubos', 'Un montón de tubos de ensallo y probetas de diferentes colores y tamaños. Sientes cierta tentación de "beber probeta".'),
('lab/p3_pasillo_genetico', 'fuente', 'Una fuente de la que brota un montón de bebida espumosa.'),
('lab/p3_pasillo_genetico', 'camilla,camillas,cuerpo,cuerpos', 'Varias camillas de hospital con cuerpos inertes cubiertos por una sábana, algunas con manchas de sangre. Dudas si quieres ´destapar camilla´ Te aterroriza ver lo que oculta la sábana.'),
('lab/camara_criogenica', 'armario', 'Un armario metálico con puertas cerradas herméticamente. En una de las puertas ves una pegatina advirtiendo de un posible peligro.');

drop table if exists object_interactions;
CREATE TABLE object_interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_name TEXT NOT NULL,
    object_name TEXT NOT NULL,
    command TEXT NOT NULL,       -- Comando asociado (como "beber", "abrir")
    effect TEXT,
    message TEXT,                 -- Mensaje al ejecutar el comando (opcional)
    cooldown INTEGER,  -- Tiempo de reutilización del comando (en segundos)
    cooldown_message TEXT DEFAULT 'Por algun motivo no puedes hacer eso ahora. Quizá esperando un poco...' -- Mensaje de cooldown
);

-- Ejemplo de inserción de interacciones
INSERT INTO object_interactions (room_name, object_name, command, effect, message, cooldown, cooldown_message) VALUES
('inicio', 'probeta', 'beber', 'vida-10', 'Engulles el contenido de la probeta y sientes un terrible ardor en el esófago', 30, 'Se te quitan las ganas de probar a beber una de esas cosas experimentales'),
('lab/p3_pasillo_genetico', 'fuente', 'beber', 'energia+5', 'La fuente burbujea suavemente mientras bebes de ella. Sientes un ligero cosquilleo en tu cuerpo.', 30, 'Bebes de la fuente, te notas algo empachad@. (vuelve a beber en % segundos)'),
('lab/p3_pasillo_genetico', 'fuente', 'romper', NULL, 'Desistes en tu intento de estropear la fuente', 0, NULL),
('lab/p3_pasillo_genetico', 'camilla', 'destapar', NULL, 'Aterrorizad@, caes al suelo', 10, 'Por experiencia, no deseas presenciar lo que hace un momento se ha visto bajo la sábana'),
('lab/camara_criogenica', 'armario', 'abrir', NULL, 'El armario está cerrado con llave.', NULL, NULL);



-- NPCS
drop table if exists npcs;
CREATE TABLE IF NOT EXISTS npcs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    display_name TEXT NOT NULL,
    alias TEXT NOT NULL,
    room TEXT NOT NULL,
    can_talk BOOLEAN DEFAULT 0,
    can_fight BOOLEAN DEFAULT 0,
    conversation TEXT, -- JSON con posibles diálogos
    pv INTEGER DEFAULT 100,
    f INTEGER DEFAULT 10,
    r INTEGER DEFAULT 10,
    a INTEGER DEFAULT 10,
    d INTEGER DEFAULT 10
);

INSERT INTO npcs (display_name, alias, room, can_talk, can_fight, conversation, pv, f, r, a, d) VALUES
('Guardia-robot', 'guardia,robot', 'inicio', 1, 1, 'Un androide de aspecto bastante humanizado. Está pintado en color blanco metalizado. En su pecho lleva imprimida una inscripción: \033[91mGua-R-DIA-P3-1\033[0m. No parece ir armado.','{"greeting": "¡Detente ahí, ciudadano!"}', 100, 15, 10, 8, 12),
('Cientí-F-ICO', 'cientifico', 'lab/farmacia', 1, 0, 'Un científico de pelo alborotado y gafas de pasta con mucho aumento. Lleva puesta una bata blanca.','{"greeting": "Estoy ocupado, no molestes."}', 50, 5, 5, 5, 5);