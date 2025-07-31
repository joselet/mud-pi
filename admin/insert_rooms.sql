-- Insertar habitaciones
INSERT INTO rooms (name, title, description) VALUES
('inicio', 'Laboratorio genético', 'Un frío laboratorio genético, lleno de tubos de ensayo y equipos científicos.'),
('lab/camara_criogenica', 'Cámara Criogénica', 'Un cuarto helado con cápsulas criogénicas alineadas contra las paredes. Cada cápsula contiene un cuerpo congelado en perfecto estado. Ves un pequeño armario tras la puerta'),
('lab/farmacia', 'Farmacia', 'Un laboratorio lleno de estanterías con frascos etiquetados con nombres incomprensibles. El aire huele a químicos fuertes y algo metálico.'),
('lab/planta1', 'Planta 1 - Laboratorio de Clonación', 'Un laboratorio con cápsulas de vidrio llenas de líquido verde. Dentro de cada cápsula flota un cuerpo humanoide en diferentes etapas de desarrollo.'),
('lab/ascensor', 'Ascensor', 'Un ascensor amplio de paredes metálicas. Parece que permite la entrada y salida de varias camillas para transportarlas a otros lugares.\nUna botonera en la pared permite seleccionar el destino.\nLos botones están bastante desgastados. Puedes ver que uno de ellos, marcado con el símbolo P3 está rodeado por un recuadro iluminado.\nUn cartel advierte: ''Uso exclusivo del personal autorizado''.'),
('lab/planta2', 'Planta 2 - Sala de Experimentación', 'Una sala amplia con mesas quirúrgicas y herramientas extrañas. Pantallas muestran datos biométricos de sujetos desconocidos.'),
('lab/p3_pasillo_genetico', 'Pasillo', 'Un pasillo oscuro y frío. A lo largo del pasillo múltiples camillas están alineadas, cada una con un cuerpo inerte cubierto por una sábana.\nAl fondo ves un ascensor. Al lado, una fuente');

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
('lab/p3_pasillo_genetico', 'ascensor', 'lab/ascensor');