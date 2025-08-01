# filepath: e:\www_develop\mud-pi\config.py

# Diccionario de alias para las salidas típicas
COMMAND_ALIASES = {
    "n": "norte",
    "s": "sur",
    "e": "este",
    "o": "oeste",
    "ne": "noreste",
    "no": "noroeste",
    "se": "sudeste",
    "so": "sudoeste",
    "ar": "arriba",
    "ab": "abajo",
    "de": "dentro",
    "fu": "fuera",
    "quitar":"abandonar"
}

# Reversed dictionary for aliases (full name -> alias)
REVERSED_COMMAND_ALIASES = {v: k for k, v in COMMAND_ALIASES.items()}

# Descripción de los niveles: infrarojo, rojo, naranja, amarillo, verde, índigo, morado, ultravioleta, x
NIVEL_DISPLAY = {
    0: "IR",
    1: "R",
    2: "N",
    3: "Y",
    4: "V",
    5: "I",
    6: "M",
    7: "UV",
    8: "X"
}

# Colores ANSI para los niveles
NIVEL_COLOR = {
    0: "\033[90m",  # IR (37)
    1: "\033[91m",  # R
    2: "\033[33m",  # N
    3: "\033[93m",  # Y
    4: "\033[92m",  # V
    5: "\033[96m",  # I (o 94)
    6: "\033[95m",  # M
    7: "\033[35m",  # UV
    8: "\033[97m",   # X
    "reset": "\033[0m"  # Reset color
}

# Servicios de destino
SERVICIOS = {
    "SSI": {
        "titulo": "**Seguridad Interna**",
        "descripcion": (
            "El **Servicio de Seguridad Interna (SSI)** se encarga de eliminar "
            "comunistas y traidores, y de mantener el orden en el Complejo Alfa. "
            "Funciona como una síntesis de policía, Servicio Secreto, Comisaría Política, "
            "Inquisición, Ministerio de la Verdad y Departamento Antinarcóticos. "
            "Sus miembros son ampliamente odiados y temidos por ciudadanos de otros servicios "
            "y sus agentes están por todas partes. El SSI continuamente infiltra agentes "
            "para verificar la lealtad de los ciudadanos y organiza operaciones de incitación "
            "para tentar a aquellos proclives a la traición. Son responsables de la "
            "detención y ejecución de traidores declarados. La mayoría de sus agentes "
            "trabajan encubiertos, pero también tienen cuerpos uniformados como las "
            "patrullas de CS Rojo, conocidas por su corpulencia y rudeza mental, cuya tarea "
            "principal es dispersar peleas entre los Infrarrojos. Los agentes de niveles "
            "superiores se ocupan de la policía secreta, vigilando conductas o pensamientos "
            "sospechosos de traición. Las patrullas Z de CS Azul son temidas por su "
            "disciplina, entrenamiento, falta de piedad y armamento mortífero."
        )
    },
    "STC": {
        "titulo": "**Servicio Técnico**",
        "descripcion": (
            "El **Servicio Técnico (STC)** se dedica al mantenimiento de robots, "
            "vehículos, medios de comunicación, hardware, sistemas industriales y de "
            "producción, y equipo electromecánico o electrónico. "
            "Sus funciones se superponen con las del SDF y SEG, lo que genera una "
            "constante rivalidad burocrática. Es el **único Servicio que puede "
            "establecer contacto ocasional con otros Complejos**, lo que a menudo "
            "conlleva la sospecha de traición para sus miembros. Son los "
            "'manitas' del Complejo, a quienes se recurre para problemas con "
            "trituradores de basura, retretes o robots mascota. A menudo se niegan "
            "a realizar reparaciones sin la documentación apropiada, lo que lleva a los "
            "ciudadanos a usar el soborno o la intimidación para obtener sus servicios. "
            "Los agentes del STC se distinguen por llevar monos especiales con bolsillos "
            "llenos de herramientas."
        )
    },
    "SBD": {
        "titulo": "**Bienestar, Desarrollo y Control Mental**",
        "descripcion": (
            "El **Servicio de Bienestar, Desarrollo y Control Mental (SBD)** es "
            "responsable de proveer los servicios básicos al ciudadano, incluyendo "
            "vivienda, guardería, educación, entretenimiento y jubilación. "
            "Es el **servicio más numeroso, pero el menos prestigioso y con menos "
            "confianza política**, debido a su estrecho contacto con las masas "
            "infrarrojas. Como encargado de la propaganda del régimen, "
            "el SBD tiene la capacidad de manipular las emociones de las masas, "
            "convirtiéndolo en el más poderoso en este aspecto. También "
            "se encarga de archivar voluminosos registros y de recomendar individuos "
            "para promoción desde las masas infrarrojas, así como de decidir su "
            "distribución en otros servicios. Es una gigantesca estructura "
            "burocrática donde el papeleo es omnipresente, y es virtualmente "
            "imposible que su personal haga algo más allá de rellenar documentos "
            "y enviar a los ciudadanos de ventanilla en ventanilla. "
            "Su disciplina y moral son algo decadentes, permitiendo un cierto relajamiento "
            "en la ortodoxia política, y es uno de los servicios donde la traición es "
            "menos perseguida."
        )
    },
    "SDF": {
        "titulo": "**Servicio de Defensa**",
        "descripcion": (
            "Las **Fuerzas Armadas y Defensa (SDF)** se encargan de la defensa del "
            "Complejo Alfa contra invasiones externas de traidores comunistas mutantes "
            "y de planear la guerra eterna contra los comunistas del mundo exterior. "
            "Además, complementan al SSI en caso de amenaza interna. "
            "El cuerpo de élite más famoso dentro del SDF es el **Escuadrón Cóndor**, "
            "admirado y respetado por los ciudadanos, compuesto por combatientes "
            "duros, bien entrenados y mejor equipados para misiones de alta prioridad. "
            "Los miembros del SDF tienen una alta moral, y el SSI les teme y respeta "
            "por su eficacia en la resolución de problemas. Existe una considerable "
            "fricción entre el SDF y el SSI, ya que el primero no coopera en el control "
            "represivo de la ortodoxia política. Los miembros del SDF a menudo son "
            "asignados temporalmente a otros servicios en misiones de seguridad y "
            "desprecian a todos los demás Servicios, excepto quizás al SID, que les "
            "proporciona tecnología fantástica."
        )
    },
    "SPL": {
        "titulo": "**Servicio de Producción y Logística**",
        "descripcion": (
            "El **Servicio de Producción y Logística (SPL)** abarca la producción "
            "agrícola e industrial, así como el almacenamiento, elaboración y "
            "distribución de todos los productos y recursos. Sus obligaciones "
            "primarias incluyen alimentar a la población y distribuir bienes de "
            "consumo. Como servicio, se encuentra ligeramente por encima del SBD "
            "en estatus. A pesar de que parece controlar la 'riqueza' del Complejo, "
            "no deja de ser otro servicio burocrático mastodóntico. Los Infrarrojos de este "
            "servicio son cocineros, camareros, granjeros y obreros de fábricas. "
            "La mayoría de sus miembros son apáticos pero razonables y prácticos, "
            "aunque ocasionalmente aparecen individuos ambiciosos, corruptos o "
            "fanáticamente dedicados a aumentar la producción y el consumo. "
            "Son conocidos por su burocracia y la dificultad para obtener materiales o "
            "reparaciones."
        )
    },
    "SEG": {
        "titulo": "**Servicio de Energía y Transporte**",
        "descripcion": (
            "El **Servicio de Energía y Transporte (SEG)** tiene la difícil tarea de "
            "mantener las antiguas plantas de energía del Complejo Alfa y los sistemas "
            "de ingeniería de control del hábitat (tráfico, depuración de agua y aire, "
            "reciclado y eliminación de basuras). La supervivencia de todo el "
            "sistema depende de su funcionamiento eficaz. Esto lo hace "
            "particularmente vulnerable a la traición y el sabotaje, resultando en "
            "una **fuerte vigilancia por parte del SSI**. Su poder le otorga "
            "un altísimo estatus, lo que genera fricción con otros servicios, pero "
            "también lo hace uno de los servicios más leales al Ordenador. "
            "Tienden a ser callados y desconfiados con miembros de otros servicios "
            "y suelen cuidarse solo a sí mismos. Otra de sus importantes "
            "funciones es la de gestionar el transporte del Complejo Alfa."
        )
    },
    "SID": {
        "titulo": "**Servicio de Investigación y Diseño**",
        "descripcion": (
            "El **Servicio de Investigación y Diseño (SID)** agrupa a una legión "
            "de genios, chiflados y científicos locos, junto con personal político "
            "y policial sin talentos especiales. El SID inventa valiosos "
            "diseños, ideas y procedimientos. Los técnicos que los "
            "inventan y desarrollan gozan de una inusual licencia de comportamiento "
            "y obtienen recursos y apoyo ilimitados para proyectos preferidos por "
            "el Ordenador, sin importar sus fracasos. Los Laboratorios de "
            "Investigación y las Áreas de Prueba son lugares muy peligrosos para "
            "los visitantes debido a la constante experimentación de alta tecnología. "
            "La investigación original es escasa; la mayor parte de su tarea consiste "
            "en rescatar tecnología arcana de siglos anteriores al ataque comunista. "
            "Su objetivo principal es el descubrimiento de nuevas armas y técnicas de "
            "combate contra los comunistas, mientras que la mejora de las condiciones "
            "de vida de los ciudadanos tiene una baja prioridad. El Ordenador "
            "es 'exasperantemente indulgente' con los miembros del SID."
        )
    },
    "SCP": {
        "titulo": "**Servicio Central de Procesamiento**",
        "descripcion": (
            "El **Servicio Central de Procesamiento (SCP)** es la autoridad central "
            "de supervisión administrativa. Es una burocracia atrincherada "
            "dedicada a manejar registros, regulaciones, ingeniería genética humana, "
            "justicia y operaciones ejecutivas. Algunos de sus agentes están "
            "directamente asignados por el Ordenador a proyectos de especial interés, "
            "gozando de autonomía y capacidad de decisión incomparables. "
            "Normalmente, se dedican a inventar nuevos procesos y formularios, rellenar "
            "papeleo, y dar conferencias y cursos, a menudo resultando en una "
            "burocracia aún más incompetente. El Ordenador apoya "
            "entusiastamente sus modernas teorías de dirección y gestión, "
            "asegurando que todos los demás servicios cumplan sus directrices. "
            "Como resultado, el personal del SCP goza del resentimiento y la "
            "desconfianza de los demás ciudadanos por este favoritismo. "
            "Tienden a abusar de su privilegio y continuamente sugieren el "
            "desagrado del Ordenador si las cosas no se hacen a su manera, siendo "
            "su principal arma la amenaza velada de un informe negativo. "
            "Siempre tienen el mejor equipo y parecen prósperos."
        )
    }
}