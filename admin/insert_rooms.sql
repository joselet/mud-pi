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
    hidden BOOLEAN DEFAULT 0, -- Nuevo campo para salidas ocultas
    FOREIGN KEY(room_name) REFERENCES rooms(name),
    FOREIGN KEY(target_room) REFERENCES rooms(name)
);

-- Insertar habitaciones
INSERT INTO rooms (name, title, description) VALUES
('inicio', 'P3: Laboratorio genético', 'Un frío laboratorio genético, lleno de tubos de ensayo y equipos científicos.'),
('lab/camara_criogenica', 'P2: Cámara Criogénica', 'Un cuarto helado con cápsulas criogénicas alineadas contra las paredes. Cada cápsula contiene un cuerpo congelado en perfecto estado. Un panel bajo cada una de las cápsulas muestra información sobre el estado del sujeto. Ves un pequeño armario tras la puerta'),
('lab/farmacia', 'P3: Farmacia', 'Un laboratorio lleno de estanterías con frascos etiquetados con nombres incomprensibles. El aire huele a químicos fuertes y algo metálico. En un rincón ves una pared llena de anotaciones junto a un pequeño terminal de datos.'),
('lab/almacen_quimico', 'P3: Almacén Químico', 'Un almacén desordenado lleno de cajas y frascos. Parece que aquí se almacenan sustancias altamente tóxicas. Ves varias estanterías repletas de botellas y recipientes etiquetados con símbolos de peligro. Un leve zumbido eléctrico llena el aire. El fluorescente de la sala parpadea ligeramente.'),
('lab/sala_control', 'P1: Sala de Control', 'Una sala de control con un montón de sillas ergonómicas frente a pantallas destellantes que muestran datos del laboratorio. Un gran mapa del laboratorio está colgado en la pared. En otra pared, un monitor de anuncios.'),
('lab/planta1', 'P1: Laboratorio de Clonación', 'Un laboratorio con cápsulas de vidrio llenas de líquido verde. Dentro de cada cápsula flota un cuerpo humanoide en diferentes etapas de desarrollo.'),
('lab/ascensor', 'Ascensor', 'Un ascensor amplio de paredes metálicas. Parece que permite la entrada y salida de varias camillas para transportarlas a otros lugares.\nUna botonera en la pared permite seleccionar el destino.\nLos botones están bastante desgastados. Puedes ver que uno de ellos, marcado con el símbolo P3 está rodeado por un recuadro iluminado.\nUn cartel advierte: ''Uso exclusivo del personal autorizado''.'),
('lab/planta2', 'P2: Sala de Experimentación', 'Una sala amplia con mesas quirúrgicas y herramientas extrañas. Pantallas muestran datos biométricos de sujetos desconocidos.'),
('lab/p3_pasillo_genetico', 'P3: Pasillo', 'Un pasillo oscuro y frío. A lo largo del pasillo múltiples camillas están alineadas, cada una con un cuerpo inerte cubierto por una sábana.\nAl fondo ves un ascensor. Al lado, una fuente'),
('respawn', 'Bañera incubadora', 'Te encuentras rodeado de líquido. Puedes respirar gracias a un tubo insertado en tus fosas nasales. Abres los ojos y apenas puedes ver el exterior. el líquido pastoso que te recubre te proporciona un calor confortable. Te quedarías aquí de por vida.'),
('lab/archivo_genetico', 'Archivo Genético', 'Te encuentras en una Unidad de Archivo Genético, un vasto espacio cavernoso donde el eco de un zumbido constante es el único sonido. La atmósfera es gélida y huele a ozono. Miles de cápsulas de contención selladas se apilan en formaciones geométricas, sus superficies metálicas reflejando la luz verdosa de paneles indicadores. En cada cápsula, una etiqueta digital proyecta un nombre seguido de un código de línea genética archivada.\nEste es el depósito permanente del Servicio Central de Procesamiento (SCP), una autoridad dedicada a la ingeniería genética humana y al manejo de registros. Aquí, el Ordenador, en su infinita sabiduría y búsqueda de la optimización de recursos para el Complejo Alfa, guarda los vestigios de lo que considera patrones biológicos inservibles. Tu propio patrón ya forma parte de esta colección silenciosa, una línea que, tras la terminación de su última réplica clónica, ha sido clasificada como recurrente y defectuosa.\nLa luz parpadeante revela un tenue letrero: "Archivo Activo - No Molestar".');


-- Insertar salidas
INSERT INTO exits (room_name, exit_name, target_room, hidden) VALUES
('inicio', 'sur', 'lab/p3_pasillo_genetico', 0),
('lab/camara_criogenica', 'oeste', 'lab/planta2', 0),
('lab/farmacia', 'norte', 'lab/p3_pasillo_genetico', 0),
('lab/farmacia', 'este', 'lab/almacen_quimico', 0), 
('lab/planta1', 'ascensor', 'lab/ascensor', 0),
('lab/planta1', 'oeste', 'lab/sala_control', 0),
('lab/ascensor', 'p3', 'lab/p3_pasillo_genetico', 0),
('lab/ascensor', 'p2', 'lab/planta2', 0),
('lab/ascensor', 'p1', 'lab/planta1', 0),
('lab/planta2', 'ascensor', 'lab/ascensor', 0),
('lab/planta2', 'este', 'lab/camara_criogenica', 0),
('lab/p3_pasillo_genetico', 'norte', 'inicio', 0),
('lab/p3_pasillo_genetico', 'sur', 'lab/farmacia', 0),
('lab/p3_pasillo_genetico', 'ascensor', 'lab/ascensor', 0),
('respawn', 'fuera', 'inicio', 0),
('lab/almacen_quimico', 'oeste', 'lab/farmacia', 0),
('lab/sala_control', 'este', 'lab/planta1', 0);







/*

-- Sentencia 2: Añadir la salida oculta desde 'lab/farmacia' a la nueva sala
-- NOTA: Se asume la existencia de una tabla 'exits' con columnas 'is_hidden', 'reveal_command' y 'reveal_object'.
-- Si tu sistema maneja la revelación de salidas de otra forma (ej. solo a través del efecto de object_interactions),
-- esta sentencia podría necesitar un ajuste o ser omitida si la salida se "crea" dinámicamente.
INSERT INTO exits (from_room, to_room, direction, is_hidden, reveal_command, reveal_object) VALUES
('lab/farmacia', 'lab/sala_archivada_clones', 'abajo', TRUE, 'activar panel_oculto', 'panel_oculto');

-- Sentencia 3: Añadir la interacción para el "panel_oculto" que revela la trampilla
-- La acción de 'activar panel_oculto' revelará la salida oculta.
INSERT INTO object_interactions (room_name, object_name, command, effect, message, cooldown, cooldown_message) VALUES
('lab/farmacia', 'panel_oculto', 'activar', 'reveal_exit:lab/sala_archivada_clones:abajo', 'Tras unos segundos de manipulación, un zumbido hidráulico te envuelve. Un segmento de suelo se desliza lateralmente, revelando una oscura rampa descendente. Una ráfaga de aire gélido y denso, con un inconfundible aroma a ozono y formaldehído, emerge de la abertura. Sabes que has encontrado algo que el Ordenador preferiría mantener oculto. Una discreta flecha verde parpadea, indicando la salida.', 0, NULL);

-- Sentencia 4: Añadir una interacción de "examinar" el suelo para dar una pista sobre el panel oculto
-- Esto ayuda a guiar al jugador sin revelar directamente el panel.
INSERT INTO object_interactions (room_name, object_name, command, effect, message, cooldown, cooldown_message) VALUES
('lab/farmacia', 'suelo', 'examinar', NULL, 'El suelo de la farmacia parece monótono y sin costuras, pero una inspección minuciosa revela marcas de desgaste inusuales cerca de una de las paredes, como si algo pesado se moviera allí con regularidad. **Podría haber un panel oculto.**', 0, NULL);

2. Objetos Observables Adicionales y Ambientación
A continuación, se proponen interacciones observar, leer, inspeccionar o estudiar para añadir más detalles descriptivos y enriquecer la atmósfera de las salas existentes. Estas interacciones se basan en el conocimiento del Complejo Alfa, el Ordenador, la paranoia y los servicios
.


-- Sala: 'lab/farmacia' [1, 13]
INSERT INTO object_interactions (room_name, object_name, command, effect, message, cooldown, cooldown_message) VALUES
('lab/farmacia', 'estanterias_frascos', 'inspeccionar', NULL, 'Altas estanterías metálicas repletas de frascos y viales de colores. Algunos contienen líquidos burbujeantes etiquetados como "**Suplemento de Felicidad**" o "**Energizante Patriótico**" [14], otros, geles y pastillas sin identificar. Huele a desinfectante y a promesas químicas.', 0, NULL),
('lab/farmacia', 'refrigerador_muestras', 'observar', NULL, 'Un robusto refrigerador industrial con una puerta de seguridad blindada y un pequeño ojo óptico que te escanea. Su zumbido constante sugiere que mantiene algo muy importante (y posiblemente traidor) a baja temperatura. Una etiqueta advierte: "**Acceso Nivel Ultravioleta - ¡Peligro Biológico!**"', 0, NULL);

-- Sala: 'lab/p3_pasillo_genetico' [15]
INSERT INTO object_interactions (room_name, object_name, command, effect, message, cooldown, cooldown_message) VALUES
('lab/p3_pasillo_genetico', 'tubos_clonacion_vacios', 'mirar', NULL, 'Grandes tubos de cristal vacíos, del tamaño de un humano, con restos de fluidos de gestación adheridos a sus paredes interiores. Huelen a ozono y a historia olvidada de miles de "túes" anteriores. Un recordatorio constante de la **naturaleza desechable de la vida en el Complejo Alfa** y la eficiencia del **sistema clónico** [5, 6, 16].', 0, NULL),
('lab/p3_pasillo_genetico', 'diagramas_geneticos', 'estudiar', NULL, 'En las paredes, paneles luminosos muestran intrincados diagramas de cadenas de ADN, con anotaciones en un complejo código de colores. Demasiado técnico y de un **nivel de seguridad superior** para tu comprensión actual [8]. Intentar descifrarlo sin la autorización adecuada sería un acto de **traición** [5, 17, 18].', 0, NULL);

-- Sala: 'lab/camara_criogenica' [19]
INSERT INTO object_interactions (room_name, object_name, command, effect, message, cooldown, cooldown_message) VALUES
('lab/camara_criogenica', 'capsulas_criogenicas', 'observar', NULL, '', 0, NULL),
('lab/camara_criogenica', 'panel_temperatura', 'examinar', NULL, '', 0, NULL);

3. Interacción Adicional de Ambientación
Para la lab/camara_criogenica, donde el armario ya está "cerrado con llave"
, podemos añadir una interacción que, en lugar de intentar forzarlo y obtener un simple mensaje, resalte la dificultad y el riesgo, reforzando el concepto de niveles de seguridad y la paranoia del juego.

-- Sala: 'lab/camara_criogenica' [19]
-- Interacción adicional para el "armario"
INSERT INTO object_interactions (room_name, object_name, command, effect, message, cooldown, cooldown_message) VALUES
('lab/camara_criogenica', 'armario', 'forzar', NULL, 'El **armario** está sólidamente construido y parece diseñado para resistir intentos de apertura no autorizados. Forzarlo probablemente activaría alguna alarma y atraería una atención no deseada del **SSI** [20, 21]. Es una cerradura de nivel Violeta; cualquier intento no autorizado de manipulación es **traición**.', 0, NULL);

*/