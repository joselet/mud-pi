drop table if exists room_objects;
CREATE TABLE room_objects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_name TEXT NOT NULL,
    object_name TEXT NOT NULL,
    description TEXT NOT NULL
);

-- Ejemplo de inserción de objetos
INSERT INTO room_objects (room_name, object_name, description) VALUES
('inicio', 'probeta,probetas', 'Diferentes probetas de cristal llenas de diferentes colores semi-transparentes, azul, verde, amarillo... Parece que contienen algún tipo de sustancia química. Te preguntas que ocurriría si pruebas a "beber probeta azul" o quizás "beber probeta verde", o "beber probeta amarilla"...'),
('inicio', 'tubo,tubos', 'Un montón de tubos de ensallo y probetas de diferentes colores y tamaños. Sientes cierta tentación de estudiar también las diferentes probetas.'),
('inicio', 'terminal,terminales', 'El científico te bloquea el acceso diciendo: "No puedes acceder a esta información."'),
('lab/farmacia', 'terminal,terminales', 'Una terminal de ordenador con una pantalla que muestra un mensaje de bienvenida. Parece que puedes "teclear terminal" para ver los comandos disponibles.'),
('lab/farmacia', 'anotacion,anotaciones,nota,notas', 'Varias notas con información diversa, nombres y números. Das especial importancia a una nota en la que pone: Acceso al terminal. "teclear password 1234.'),
('lab/p3_pasillo_genetico', 'pasillo, pasillos', 'Un pasillo largo y estrecho lleno de tubos de ensayo y probetas. El ambiente es frío y silencioso.'),
('lab/p3_pasillo_genetico', 'fuente', 'Una fuente de la que brota un montón de bebida espumosa refrescante. Parece que podrías "beber fuente" para refrescarte un poco.'),
('lab/p3_pasillo_genetico', 'camilla,camillas,cuerpo,cuerpos', 'Varias camillas de hospital con cuerpos inertes cubiertos por una sábana, algunas con manchas de sangre. Dudas si quieres ´destapar camilla´ Te aterroriza ver lo que oculta la sábana.'),
('lab/sala_control', 'mapa', 'Un gran mapa táctico del laboratorio cuelga prominentemente en una de las paredes, delineando líneas de tráfico y zonas de acceso. Algunas secciones del mapa parpadean ominosamente en colores de nivel superior, inaccesibles para los de tu credencial.'),
('lab/sala_control', 'monitor,monitores', 'Dominando otra pared, un monitor de anuncios prominente interrumpe los flujos de datos con destellos de propaganda y avisos del Ordenador, como el lapidario recordatorio: "¡Sé feliz! ¡La traición es enfermedad! ¡Tu amigo el Ordenador te vigila y te ama! ¡Recuerda activar tu siguiente clon si es necesario!". Estos mensajes refuerzan la constante amenaza de la ejecución sumaria por cualquier indicio de deslealtad.'),
('lab/sala_control', 'silla,sillas', 'Frente a las consolas, se encuentran varias sillas ergonómicas de diseño estándar del Complejo Alfa [User Provided]. A pesar de su apariencia funcional, parecen diseñadas para "maximizar la productividad y minimizar la comodidad excesiva", un principio reforzado por el mensaje grabado en sus reposabrazos: "La incomodidad es traición"'),
('lab/sala_control', 'ordenador,ordenadores', 'Un ordenador central que parece controlar todo el laboratorio. Está conectado a varios monitores y dispositivos de seguridad.'),
('lab/sala_control', 'ordenador,ordenadores,pantalla,pantallas', 'Varias pantallas de datos incomprensibles. Algunas muestran información sobre el estado del laboratorio, otras parecen ser monitores de seguridad.'),
('lab/camara_criogenica', 'armario', 'Un armario metálico con puertas cerradas herméticamente. En una de las puertas ves una pegatina advirtiendo de un posible peligro.'),
('lab/camara_criogenica','capsulas','Múltiples cápsulas verticales, algunas transparentes, mostrando figuras humanoides suspendidas en un líquido translúcido. Son **líneas genéticas inactivas**, esperando su activación. Un escalofrío te recorre al pensar que tu propia réplica podría estar ahí, o la de algún traidor ya **archivado**. El aire helado indica su propósito de conservación... o de olvido.'),
('lab/camara_criogenica','panel,paneles','Un panel de control digital con múltiples lecturas de temperatura y presión, custodiado por una carcasa blindada. La interfaz es compleja y está bloqueada. Un intento de manipularlo sin autorización sería, sin duda, una **traición de alto nivel**. La temperatura interna marca -150°C. **El Ordenador es su amigo.**');

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
('inicio', 'probeta azul', 'beber', 'pv-=15', 'Engulles el contenido de la probeta y sientes un terrible ardor en el esófago', 30, 'Se te quitan las ganas de probar a beber una de esas cosas experimentales'),
('inicio', 'probeta verde', 'beber', NULL, 'Engulles el contenido de la probeta. El amargor extremo te produce nauseas', 30, 'Se te quitan las ganas de probar ese liquido tan asqueroso nuevamenta'),
('inicio', 'probeta amarilla', 'beber', 'pv+=10', 'Engulles el contenido de la probeta sintiendo un generoso restablecimiento', 30, 'No te convence abusar de las probetas amarillas, pero te sientes mejor. (vuelve a beber en % segundos)'),
('lab/farmacia', 'terminal', 'teclear', NULL, 'La terminal muestra un prompt solicitando una contraseña', 0, NULL),
('lab/farmacia', 'password 1234', 'teclear', NULL, 'La terminal muestra un mensaje de bienvenida al inventario general de Farmacia:\nINVENTARIO DE FARMACIA:\nStock de medicamentos: 10\nStock de suministros: 5\n\nPara volver al menú principal, "teclear menu principal"', 0, NULL),
('lab/farmacia', 'inventario', 'teclear', NULL, 'La terminal muestra un mensaje de bienvenida al inventario general de Farmacia:\nINVENTARIO DE FARMACIA:\nStock de medicamentos: 10\nStock de suministros: 5\n\nPara volver al menú principal, "teclear menu principal"', 0, NULL),
('lab/farmacia', 'menu principal', 'teclear', NULL, 'SISTEMA DE INFORMACION GENERAL. (COMPLEJO ALFA, SECTOR LAB)\nComandos disponibles:\n- ayuda (para ver la ayuda disponible)\n- inventario (para mostrar el inventario de farmacia)\n- informacion general (para ver la informacion general del Complejo Alfa).\n\nsintaxis: "teclear <comando>"', 0, NULL),
('lab/farmacia', 'ayuda', 'teclear', NULL, 'SISTEMA DE AYUDA DE TERMINALES DE DATOS. (COMPLEJO ALFA, SECTOR LAB)\nUtiliza "teclear <comando>" para interactuar con el terminal.\nPara acceder al menú principal utiliza "teclear menu principal".', 0, NULL),
('lab/p3_pasillo_genetico', 'fuente', 'beber', 'e+=15', 'La fuente burbujea suavemente mientras bebes de ella. Sientes un ligero cosquilleo en tu cuerpo.', 30, 'Bebes de la fuente, te notas algo empachad@. (vuelve a beber en % segundos)'),
('lab/p3_pasillo_genetico', 'fuente', 'romper', NULL, 'Desistes en tu intento de estropear la fuente', 0, NULL),
('lab/p3_pasillo_genetico', 'camilla', 'destapar', NULL, 'Aterrorizad@, caes al suelo', 10, 'Por experiencia, no deseas presenciar lo que hace un momento se ha visto bajo la sábana'),
('lab/camara_criogenica', 'armario', 'abrir', NULL, 'El armario está cerrado con llave.', NULL, NULL);

-- Entrada para el comando "teclear informacion general"
INSERT INTO object_interactions (room_name, object_name, command, effect, message, cooldown, cooldown_message) VALUES
('lab/farmacia', 'informacion general', 'teclear', NULL, 'SISTEMA DE INFORMACION GENERAL. (COMPLEJO ALFA, SECTOR LAB)\n\nSaludos, ciudadano. Te encuentras en el Complejo Alfa, tu hogar, una **utopía perfecta** donde no hay guerras, hambre ni enfermedades, y **eres feliz** [1, 2]. Esto es así porque el Complejo Alfa está gobernado por el benévolo **Ordenador**, **tu amigo**, que se asegura de satisfacer todas tus necesidades y de que seas feliz [1, 3, 4].\n\nTu identidad es la de un **clon**, gestado en bancos de clonación, parte de una generación de seis seres idénticos [2, 3]. El Ordenador asegura las copias de respaldo para tu continuidad [3].\n\nSin embargo, el Complejo Alfa está en **guerra constante**. Existen peligros de infiltración de enemigos como los **comunistas**, y de **traidores** internos como los **mutantes** y miembros de **Sociedades Secretas**, que deben ser desenmascarados y eliminados. ¡**Mantente alerta** y no confíes en nadie! [4, 5] El Ordenador te protege, y **denunciar la traición es tu deber** [5].\n\nTodos los ciudadanos poseen un **Código de Seguridad (CS)** que determina su nivel y privilegios. Revisa tu CS.\nSi tu CS actual es **Rojo**, lo que te permite acceso a áreas rojas y negras [6, 7]\nSi tu CS actual es **Infra-Rojo**, únicamente te permite acceso a áreas sin color [6, 7].\nDesobedecer las normas de CS o no llevar el uniforme de tu color es **traición** [7, 8].\n\nEl Complejo se organiza en **ocho Servicios**, semejantes a ministerios, cada uno con funciones esenciales pero en continua pugna por recursos. Es fundamental comprender tu rol dentro de ellos [7, 9].\n\nComandos relacionados:\n- normas\n- servicios\n- ordenador\n- \033[35mmutantes\033[0m\n- \033[35msociedades secretas\033[0m', 0, NULL);

-- Entrada para el comando "teclear ordenador"
INSERT INTO object_interactions (room_name, object_name, command, effect, message, cooldown, cooldown_message) VALUES
('lab/farmacia', 'ordenador', 'teclear', NULL, 'SISTEMA DE INFORMACION GENERAL. (COMPLEJO ALFA, SECTOR LAB)\n\nEl **Ordenador** es la entidad **omnisciente y benévola** que gobierna y protege el Complejo Alfa, **tu amigo** [1, 3]. Está diseñado para satisfacer todas tus necesidades y asegurar tu felicidad, monitoreando cada aspecto de tu vida para tu bienestar [4, 10].\n\nEl Ordenador está constantemente alerta a las amenazas, temiendo a todos los enemigos y viendo **conspiraciones o sabotajes** detrás de cualquier problema [11]. Tu **lealtad** es su mayor preocupación [11]. Recuerda que Él te observa constantemente para tu protección; la **traición se castiga con la ejecución sumaria** [2, 12, 13].', 0, NULL);

-- Entrada para el comando "teclear normas"
INSERT INTO object_interactions (room_name, object_name, command, effect, message, cooldown, cooldown_message) VALUES
('lab/farmacia', 'normas', 'teclear', NULL, 'SISTEMA DE INFORMACION GENERAL. (COMPLEJO ALFA, SECTOR LAB)\n\nPara mantener la **utopía** del Complejo Alfa, todos los ciudadanos deben adherirse estrictamente a las normas [1, 14]. La **felicidad es un estado obligatorio**; la infelicidad es **traición** y puede ser castigada con la ejecución sumaria [2].\n\nDebes llevar en todo momento el **uniforme del color de tu Código de Seguridad (CS)**, y solo puedes penetrar en áreas pintadas con tu CS o uno inferior [7, 8]. No hacerlo es **traición** [7, 8].\n\nCualquier acto de deslealtad hacia el Ordenador o sus representantes, como cuestionar su juicio, dañar material, usar poderes mutantes (si los tuvieras), conspirar, o mostrar indicios de pertenencia a una sociedad secreta, son considerados **traición** y acumularán Puntos de Traición, llevando a sanciones severas o incluso a la ejecución [12, 15]. **Confía siempre en el Ordenador**, tu amigo y protector [3].', 0, NULL);

-- Entrada para el comando "teclear mutantes" (conocimiento clasificado)
INSERT INTO object_interactions (room_name, object_name, command, effect, message, cooldown, cooldown_message) VALUES
('lab/farmacia', 'mutantes', 'teclear', 'traicion+=1', '¡**INFORMACIÓN CLASIFICADA: ACCESO NO AUTORIZADO**! (COMPLEJO ALFA, SECTOR LAB)\n\nCiudadano, el **conocimiento excesivo sobre los poderes mutantes** es considerada **traición** y está clasificado a nivel Ultravioleta, inaccesible para tu CS Rojo [16, 17].\n\nLos **mutantes son traidores** potenciales o declarados que deben ser desenmascarados y eliminados por la seguridad del Complejo [4, 18]. Algunos poderes mutantes son tan peligrosos que revelarlos conlleva una **sentencia de muerte inmediata** [19, 20].\n\n(Se te ha asignado un **Punto de Traición** por intentar acceder a esta información clasificada [15, 21]. El Ordenador es tu amigo y vela por tu lealtad [3].)','300', 'El Ordenador ha notado tu interés inusual en los mutantes. Se te aconseja discreción y lealtad.\n(Info cooldown) Puedes volver a intentar teclear este comando en % segundos.');

-- Entrada para el comando "teclear sociedades secretas" (conocimiento clasificado)
INSERT INTO object_interactions (room_name, object_name, command, effect, message, cooldown, cooldown_message) VALUES
('lab/farmacia', 'sociedades secretas', 'teclear', 'traicion+=1', '¡**INFORMACIÓN CLASIFICADA: ACCESO NO AUTORIZADO**! (COMPLEJO ALFA, SECTOR LAB)\n\nCiudadano, ser miembro de una **Sociedad Secreta es alta traición** y la condena más normal es la muerte si el Ordenador se entera [16]. El **conocimiento excesivo sobre las sociedades secretas** implica pertenencia a ellas, lo que se castiga con la **ejecución sumaria** [5].\n\nEstas organizaciones buscan subvertir la lealtad al Ordenador y al Complejo, y sus miembros, así como los mutantes, son **traidores que deben ser denunciados** [4, 5]. Incluso otras sociedades secretas pueden ser enemigas de la tuya [5].\n\n(Se te ha asignado un **Punto de Traición** por intentar acceder a esta información clasificada [15, 21]. El Ordenador es tu amigo y vela por tu lealtad [3].)','300', 'El Ordenador ha notado tu interés inusual en las Sociedades Secretas. Se te aconseja discreción y lealtad.\n(Info cooldown) Puedes volver a intentar teclear este comando en % segundos.');

-- Entrada para el comando "teclear servicios"
INSERT INTO object_interactions (room_name, object_name, command, effect, message, cooldown, cooldown_message) VALUES
('lab/farmacia', 'servicios', 'teclear', NULL, 'SISTEMA DE INFORMACION GENERAL. (COMPLEJO ALFA, SECTOR LAB)\n\nEl Complejo Alfa opera a través de **ocho vitales Servicios**, cada uno con una responsabilidad única y esencial para tu bienestar [7, 9]. Aunque están en **continua pugna** por el control de fondos y personal, todos sirven al Ordenador para mantener la utopía [9]. Estos son:\n\n- **SSI: Seguridad Interna**: Se encarga de la ley y el orden, cazando y eliminando traidores. Combina funciones de policía y policía secreta [9, 22].\n- **STC: Servicio Técnico**: Responsable del mantenimiento de robots, vehículos y sistemas electrónicos. Los "manitas" del Complejo [23, 24].\n- **SBD: Bienestar, Desarrollo y Control Mental**: Provee servicios básicos como vivienda, educación y entretenimiento, además de encargarse de la propaganda del régimen [25, 26].\n- **SDF: Servicio de Defensa**: Defiende el Complejo de invasiones externas y apoya al SSI en amenazas internas. Incluye cuerpos de élite como el Escuadrón Cóndor [27, 28].\n- **SPL: Producción y Logística**: Se encarga de la producción agrícola e industrial, así como el almacenamiento y distribución de recursos para alimentar a la población [29, 30].\n- **SEG: Servicio de Energía y Transporte**: Su misión es mantener las plantas de energía y sistemas de control del hábitat, como el tráfico y la depuración de agua [29, 31].\n- **SID: Investigación y Diseño**: Desarrolla nuevas tecnologías y mecanismos para el Ordenador y los ciudadanos, a menudo rescatando tecnología de la Antigua Era [32, 33].\n- **SCP: Servicio Central de Procesamiento**: La autoridad central de supervisión administrativa, dedicada a mejorar la gestión de los Servicios y manejar registros [32, 34].', 0, NULL);

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
    "unlock": ["ocupado"],
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