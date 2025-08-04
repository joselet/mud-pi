drop table if exists rooms;
-- Tabla de habitaciones
CREATE TABLE IF NOT EXISTS rooms (
    name TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL
);

drop table if exists exits;
-- Tabla de salidas
CREATE TABLE IF NOT EXISTS exits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_name TEXT NOT NULL,
    exit_name TEXT NOT NULL,
    target_room TEXT NOT NULL,
    FOREIGN KEY(room_name) REFERENCES rooms(name),
    FOREIGN KEY(target_room) REFERENCES rooms(name)
);

-- Insertar habitaciones
INSERT INTO rooms (name, title, description) VALUES
('inicio', 'P3: Laboratorio genético', 'Un frío laboratorio genético, lleno de tubos de ensayo y equipos científicos.'),
('lab/camara_criogenica', 'P2: Cámara Criogénica', 'Un cuarto helado con cápsulas criogénicas alineadas contra las paredes. Cada cápsula contiene un cuerpo congelado en perfecto estado. Ves un pequeño armario tras la puerta'),
('lab/farmacia', 'P3: Farmacia', 'Un laboratorio lleno de estanterías con frascos etiquetados con nombres incomprensibles. El aire huele a químicos fuertes y algo metálico. En un rincón ves un pequeño terminal de datos.'),
('lab/almacen_quimico', 'P3: Almacén Químico', 'Un almacén desordenado lleno de cajas y frascos. Parece que aquí se almacenan sustancias altamente tóxicas. Ves varias estanterías repletas de botellas y recipientes etiquetados con símbolos de peligro. Un leve zumbido eléctrico llena el aire. El fluorescente de la sala parpadea ligeramente.'),
('lab/sala_control', 'P1: Sala de Control', 'Una sala de control con pantallas que muestran datos del laboratorio. Un gran mapa del laboratorio está colgado en la pared.'),
('lab/planta1', 'P1: Laboratorio de Clonación', 'Un laboratorio con cápsulas de vidrio llenas de líquido verde. Dentro de cada cápsula flota un cuerpo humanoide en diferentes etapas de desarrollo.'),
('lab/ascensor', 'Ascensor', 'Un ascensor amplio de paredes metálicas. Parece que permite la entrada y salida de varias camillas para transportarlas a otros lugares.\nUna botonera en la pared permite seleccionar el destino.\nLos botones están bastante desgastados. Puedes ver que uno de ellos, marcado con el símbolo P3 está rodeado por un recuadro iluminado.\nUn cartel advierte: ''Uso exclusivo del personal autorizado''.'),
('lab/planta2', 'P2: Sala de Experimentación', 'Una sala amplia con mesas quirúrgicas y herramientas extrañas. Pantallas muestran datos biométricos de sujetos desconocidos.'),
('lab/p3_pasillo_genetico', 'P3: Pasillo', 'Un pasillo oscuro y frío. A lo largo del pasillo múltiples camillas están alineadas, cada una con un cuerpo inerte cubierto por una sábana.\nAl fondo ves un ascensor. Al lado, una fuente'),
('respawn', 'Bañera incubadora', 'Te encuentras rodeado de líquido. Puedes respirar gracias a un tubo insertado en tus fosas nasales. Abres los ojos y apenas puedes ver el exterior. el líquido pastoso que te recubre te proporciona un calor confortable. Te quedarías aquí de por vida.');

-- Insertar salidas
INSERT INTO exits (room_name, exit_name, target_room) VALUES
('inicio', 'sur', 'lab/p3_pasillo_genetico'),

('lab/camara_criogenica', 'oeste', 'lab/planta2'),

('lab/farmacia', 'norte', 'lab/p3_pasillo_genetico'),
('lab/farmacia', 'este', 'lab/almacen_quimico'),

('lab/planta1', 'ascensor', 'lab/ascensor'),
('lab/planta1', 'oeste', 'lab/sala_control'),

('lab/ascensor', 'p3', 'lab/p3_pasillo_genetico'),
('lab/ascensor', 'p2', 'lab/planta2'),
('lab/ascensor', 'p1', 'lab/planta1'),

('lab/planta2', 'ascensor', 'lab/ascensor'),
('lab/planta2', 'este', 'lab/camara_criogenica'),

('lab/p3_pasillo_genetico', 'norte', 'inicio'),
('lab/p3_pasillo_genetico', 'sur', 'lab/farmacia'),
('lab/p3_pasillo_genetico', 'ascensor', 'lab/ascensor'),

('respawn', 'fuera', 'inicio'),
('lab/almacen_quimico', 'oeste', 'lab/farmacia'),
('lab/sala_control', 'este', 'lab/planta1');