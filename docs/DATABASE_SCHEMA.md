# Esquema de Base de Datos (SQLite)

El juego utiliza una base de datos relacional (`data/mud.db`) para persistir el mundo y los jugadores.

## 1. Tablas de Jugadores

### `players`
Almacena la ficha completa de los usuarios.
*   **Identificación**: `name` (PK), `password`.
*   **Estado**: `pv` (vida), `e` (energía), `room` (sala actual).
*   **Atributos**: `f` (fuerza), `a` (agilidad), `d` (destreza), `r` (resistencia), `p` (percepción), `c` (cinismo), `tm` (talento mecánico), `pm` (poder mutante).
*   **Lore**: `servicio` (facción), `sector`, `sociedad_secreta`, `clon` (número de clon actual), `traicion` (nivel de búsqueda), `nivel` (CS).
*   **JSON**: `config` (preferencias de usuario), `inventario` (objetos), `last_used` (cooldowns).

## 2. Tablas del Mundo (Estáticas)

### `rooms`
Definición de las salas.
*   **`name`**: ID único de texto (ej: "inicio", "lab/farmacia").
*   **`title`**: Nombre visible para el jugador.
*   **`description`**: Texto largo descriptivo.

### `exits`
Conexiones entre salas.
*   **`id`**: PK Autoincremental.
*   **`room_name`**: Sala origen (FK -> rooms.name).
*   **`exit_name`**: Comando para salir (ej: "norte", "ascensor").
*   **`target_room`**: Sala destino (FK -> rooms.name).
*   **`hidden`**: Booleano (0/1) para salidas secretas.

### `room_objects`
Objetos decorativos o interactivos visibles en las salas.
*   **`id`**: PK Autoincremental.
*   **`room_name`**: Sala donde se encuentra.
*   **`object_name`**: Nombre y alias separados por comas (ej: "probeta,probetas").
*   **`description`**: Texto que se muestra al hacer "mirar objeto".

### `object_interactions`
Define la lógica de los objetos (scripts simples).
*   **`id`**: PK Autoincremental.
*   **`room_name`**: Sala donde aplica.
*   **`object_name`**: Objeto al que aplica.
*   **`command`**: Verbo de acción (ej: "beber", "teclear").
*   **`effect`**: Código Python simple a ejecutar (ej: `pv+=10`, `e-=5`).
*   **`message`**: Texto a mostrar al jugador tras el éxito.
*   **`cooldown`**: Tiempo de espera en segundos para volver a usarlo.
*   **`cooldown_message`**: Mensaje si se intenta usar antes de tiempo.

## 3. Tablas de NPCs

### `npcs`
Personajes no jugadores (enemigos o aliados).
*   **`id`**: Identificador numérico.
*   **`display_name`**: Nombre visible.
*   **`room`**: Ubicación actual.
*   **`pv`, `pv_max`**: Puntos de vida.
*   **`f`, `a`, `d`, `r`**: Atributos de combate.
*   **`conversation`**: JSON con árbol de diálogo y temas.
*   **`can_fight`**: Booleano (si se puede atacar).
*   **`can_talk`**: Booleano (si se puede hablar).
*   **`respawn_time`**: Tiempo en segundos para revivir tras morir.
*   **`dead_message`**: Mensaje que se muestra al morir.
*   **`dead_effect`**: Efecto que se aplica al asesino (ej: ganar XP o items).