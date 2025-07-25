-- Insertar habitaciones adicionales
INSERT INTO rooms (name, title, description) VALUES
('respawn', 'Bañera incubadora', 'Te encuentras rodeado de líquido. Puedes respirar gracias a un tubo insertado en tus fosas nasales. Abres los ojos y apenas puedes ver el exterior. el líquido pastoso que te recubre te proporciona un calor confortable. Te quedarías aquí de por vida.'),
('lab/almacen_quimico', 'Almacén Químico', 'Un cuarto pequeño con estanterías repletas de botellas y recipientes etiquetados con símbolos de peligro. Un leve zumbido eléctrico llena el aire.'),
('lab/sala_control', 'Sala de Control', 'Una sala llena de pantallas y paneles de control. Luces parpadeantes indican el estado de los experimentos en curso. Un gran ventanal permite observar el laboratorio de clonación.');

-- Insertar salidas adicionales
INSERT INTO exits (room_name, exit_name, target_room) VALUES
('respawn', 'fuera', 'inicio'),
('lab/almacen_quimico', 'oeste', 'lab/farmacia'),
('lab/sala_control', 'este', 'lab/planta1');