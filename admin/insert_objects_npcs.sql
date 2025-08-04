drop table if exists room_objects;
CREATE TABLE room_objects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_name TEXT NOT NULL,
    object_name TEXT NOT NULL,
    description TEXT NOT NULL
);

-- Ejemplo de inserción de objetos
INSERT INTO room_objects (room_name, object_name, description) VALUES
('inicio', 'probeta,probetas', 'Diferentes probetas de cristal llenas de diferentes colores semi-transparentes, azul, verde, amarillo... Parece que contienen algún tipo de sustancia química. Te preguntas que ocurriría si pruebas a "beber probeta azul" o quizás "beber probeta verde"...'),
('inicio', 'tubo,tubos', 'Un montón de tubos de ensallo y probetas de diferentes colores y tamaños. Sientes cierta tentación de estudiar también las diferentes probetas.'),
('inicio', 'terminal,terminales', 'El científico te bloquea el acceso diciendo: "No puedes acceder a esta información."'),
('lab/farmacia', 'terminal,terminales', 'Una terminal de ordenador con una pantalla que muestra un mensaje de bienvenida. Parece que puedes "teclear terminal" para ver los comandos disponibles.'),
('lab/p3_pasillo_genetico', 'pasillo, pasillos', 'Un pasillo largo y estrecho lleno de tubos de ensayo y probetas. El ambiente es frío y silencioso.'),
('lab/p3_pasillo_genetico', 'fuente', 'Una fuente de la que brota un montón de bebida espumosa refrescante. Parece que podrías "beber fuente" para refrescarte un poco.'),
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
('inicio', 'probeta azul', 'beber', 'pv-=10', 'Engulles el contenido de la probeta y sientes un terrible ardor en el esófago', 30, 'Se te quitan las ganas de probar a beber una de esas cosas experimentales'),
('inicio', 'probeta verde', 'beber', NULL, 'Engulles el contenido de la probeta. El amargor extremo te produce nauseas', 30, 'Se te quitan las ganas de probar ese liquido tan asqueroso nuevamenta'),
('inicio', 'probeta amarilla', 'beber', 'pv+=10', 'Engulles el contenido de la probeta sintiendo un generoso restablecimiento', 30, 'No te convence abusar de las probetas amarillas, pero te sientes mejor. (vuelve a beber en % segundos)'),
('lab/farmacia', 'terminal', 'teclear', NULL, 'La terminal muestra un mensaje de bienvenida al inventario general de Farmacia', 0, NULL),
('lab/p3_pasillo_genetico', 'fuente', 'beber', 'e+=15', 'La fuente burbujea suavemente mientras bebes de ella. Sientes un ligero cosquilleo en tu cuerpo.', 30, 'Bebes de la fuente, te notas algo empachad@. (vuelve a beber en % segundos)'),
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
    description TEXT NOT NULL, -- Descripción del NPC
    conversation TEXT, -- JSON con posibles diálogos
    pv INTEGER DEFAULT 100,
    pv_max INTEGER DEFAULT 100,
    f INTEGER DEFAULT 10,
    r INTEGER DEFAULT 10,
    a INTEGER DEFAULT 10,
    d INTEGER DEFAULT 10,
    dead_message TEXT DEFAULT 'tu enemigo muere horriblemente.',
    dead_effect TEXT, -- Efecto al morir, recompensa o penalizacion
    dead_effect_message TEXT, -- Mensaje al aplicar el efecto
    respawn_time INTEGER DEFAULT 3600 -- Tiempo en segundos para que el NPC vuelva a aparecer
);

INSERT INTO npcs (display_name, alias, room, can_talk, can_fight, description, conversation, pv, pv_max, f, r, a, d, dead_message, dead_effect, dead_effect_message, respawn_time) VALUES
('Guardia-robot', 'guardia,robot', 'inicio', 1, 1, 'Un androide de aspecto bastante humanizado. Está pintado en color blanco metalizado. En su pecho lleva imprimida una inscripción: \033[91mGua-R-DIA-P3-1\033[0m. No parece ir armado.','{"greeting": "¡Detente ahí, ciudadano!"}', 100, 100, 15, 10, 8, 12, 'El guardia-robot colapsa en un montón de chispas.\nUn sonido de alarma retumba en toda la sala. La voz del ordenador se escucha por todos los altavoces de la zona.\nAtención: Se ha producido una grave traición en el sector del laboratorio genético. Envien rápidamente un Guardia-robot de reconocimiento y establezcan un perímetro de seguridad.', 'traicion+=1', 'El ordenador ha detectado tu traición. Has perdido algo de confianza (traicion + 1)', 60);
INSERT INTO npcs (display_name, alias, room, can_talk, can_fight, description, conversation, pv, pv_max, f, r, a, d, dead_message, dead_effect, dead_effect_message, respawn_time) VALUES
('Cient-I-FICO', 'cientifico', 'inicio', 1, 0, 'Un científico de pelo alborotado y gafas de pasta con mucho aumento. Lleva puesta una bata blanca. Se encuentra concentrado consultando datos en un terminal informático.',
'{
    "greeting": "Estoy ´ocupado´, no molestes.",
    "topics": {
        "ocupado": {
            "response": "Bien, veo que no respetas a un científico ocupado. ¿En qué te puedo ´ayudar´?",
            "unlock": ["ayudar"]
        },
        "ayudar": {
            "response": "Muchos como tú piden ayuda. En lo único que puedo ayudarte es a recuperar algo de ´fortaleza´. Otros vienen cansados y necesitan más ´energia´",
            "unlock": ["fortaleza","energia"]
        },
        "fortaleza": {
            "response": "Si quieres recuperar algo de fortaleza, te recomiendo que mires todos estos tubos y probetas. Estoy desarrollando algunas con varios efectos interesantes, te recomiendo que pruebes el compuesto de color amarillo.",
            "unlock": []
        },
        "energia": {
            "response": "Si necesitas energía, prueba a beber de la fuente en el pasillo genético.",
            "unlock": []
        }
    }
}', 50, 50, 5, 5, 5, 5, 'El científico cae al suelo, inerte.', NULL, NULL, 3600);