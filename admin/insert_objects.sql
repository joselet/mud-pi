CREATE TABLE room_objects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_name TEXT NOT NULL,
    object_name TEXT NOT NULL,
    description TEXT NOT NULL,
    interaction_command TEXT, -- Comando interactivo (opcional, como "beber")
    interaction_effect TEXT   -- Efecto del comando (opcional, como "energia+5")
    interaction_message TEXT   -- Texto del Efecto del comando (opcional, como "Te sientes revitalizado")
);

-- Ejemplo de inserción de objetos
INSERT INTO room_objects (room_name, object_name, description, interaction_command, interaction_effect) VALUES
('lab/p3_pasillo_genetico', 'fuente', 'Una fuente de la que brota un montón de bebida espumosa.', 'beber', 'energia+5'),
('lab/camara_criogenica', 'armario', 'Un armario metálico con puertas cerradas herméticamente. En una de las puertas ves una pegatina advirtiendo de un posible peligro.', NULL, NULL);