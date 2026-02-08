# Referencia Técnica de Módulos (Core)

## 1. `mud_game.py`
**Clase: `MudGame`**
Es el controlador central. Mantiene referencias a todos los subsistemas y orquesta el flujo.

*   **`__init__`**: Inicializa la conexión a la BD y crea instancias de `MudServer`, `PlayerManager`, `RoomManager`, `CombatSystem`, etc. Se pasa a sí mismo (`self`) a los gestores para que estos puedan acceder al estado global.
*   **`run()`**: El bucle principal (`while True`). Llama a las funciones de actualización.
*   **`handle_new_players()`**: Detecta conexiones nuevas y solicita el nombre.
*   **`handle_commands()`**: El "cerebro" del intérprete.
    *   Gestiona el login/creación de personaje.
    *   Interpreta comandos base: `ir`, `mirar`, `decir`, `matar`, `ficha`, `config`, `hablar`.
    *   Delega comandos desconocidos a `RoomCommandProcessor`.

## 2. `mudserver.py`
**Clase: `MudServer`**
Maneja la red pura. No sabe nada de "juego", solo de "clientes" y "mensajes".

*   **`update()`**: Revisa sockets para ver si hay nuevos datos.
*   **`get_new_players()`**: Devuelve IDs de nuevas conexiones.
*   **`get_commands()`**: Devuelve una lista de tuplas `(id, comando, parametros)` limpias.
*   **`send_message(id, msg)`**: Envía texto a un jugador específico.
*   **`_process_sent_data()`**: Limpia caracteres de control Telnet.

## 3. `room_manager.py`
**Clase: `RoomManager`**
Encargado del mundo físico.

*   **`load_room(name)`**: Carga datos de una sala desde la BD (título, descripción, salidas, objetos) y los guarda en caché.
*   **`show_room_to_player(id)`**: Envía la descripción de la sala al jugador, incluyendo quién más está allí y qué NPCs hay. Respeta la configuración `detallado` del jugador.
*   **`move_player(id, exit)`**: Mueve al jugador de una sala a otra, notificando a los presentes en la sala de origen y destino.
*   **`load_npcs_in_room(room)`**: Obtiene los NPCs vivos de una sala.
*   **`save_npc(npc)`**: Guarda el estado (vida, posición) de un NPC en la BD.

## 4. `player_manager.py`
**Clase: `PlayerManager`**
Gestión de datos persistentes de los jugadores (CRUD).

*   **`create_player(name, pass)`**: Genera un nuevo personaje con estadísticas aleatorias (Fuerza, Agilidad, etc.), asigna un Servicio, Sector y Sociedad Secreta aleatorios, y lo guarda en SQL.
*   **`load_player(name)`**: Carga la ficha completa desde la BD.
*   **`save_player(ficha)`**: Guarda los cambios (vida, xp, inventario, posición) en la BD.
*   **`validate_password()`**: Comprobación de seguridad.

## 5. `combat_system.py`
**Clase: `CombatSystem`**
Sistema de combate por turnos asíncronos.

*   **`start_combat(attacker, victim)`**: Inicia combate PvP.
*   **`start_combat_with_npc(player, npc)`**: Inicia combate PvE.
*   **`process_turn(attacker_id)`**: Ejecuta un turno de ataque.
    *   Calcula tiradas (Destreza + 1d6 vs Agilidad + 1d6).
    *   Aplica daño.
    *   Programa el siguiente turno usando `Timer`.
*   **`npc_attack(npc_id, player_id)`**: Lógica para que el NPC ataque al jugador.
*   **`end_combat...`**: Gestiona la muerte, mensajes de victoria/derrota y el sistema de clones (respawn). Si mueres 6 veces, tu personaje se archiva (Game Over real).

## 6. `effect_manager.py`
**Clase: `EffectManager`**
Permite que los objetos de la BD tengan efectos programables.

*   **`apply_effect(player_id, effect_str)`**: Recibe un string como `"pv += 10"` o `"e -= 5"`.
    *   Crea un contexto seguro con las variables del jugador.
    *   Ejecuta el string usando `exec()`.
    *   Actualiza la ficha del jugador y la guarda.

## 7. `room_command_processor.py`
**Clase: `RoomCommandProcessor`**
Maneja interacciones con objetos (ej: "beber fuente").

*   **`process_command(id, cmd, params)`**:
    1.  Busca si en la sala actual hay una interacción definida para ese comando (ej: `beber` + `probeta azul`).
    2.  Verifica el **Cooldown** (tiempo de espera).
    3.  Si es válido, llama a `EffectManager` para aplicar el efecto y muestra el mensaje configurado.

## 8. `npc_manager.py`
Módulo de utilidades para NPCs.

*   **`schedule_npc_respawn(...)`**: Usa un hilo (`threading.Timer`) para revivir a un NPC después de X segundos de haber muerto.

## 9. `config.py`
Archivo de configuración estática.

*   **`COMMAND_ALIASES`**: Diccionario para traducir `n` -> `norte`, `i` -> `inventario`, etc.
*   **`SERVICIOS`**: Descripciones de lore del juego (SSI, STC, etc.).
*   **`NIVEL_COLOR`**: Códigos ANSI para colorear los nombres según el nivel de seguridad (Rojo, Naranja, Ultravioleta...).

## 10. `timer.py`
**Clase: `Timer`**
Utilidad para manejar eventos diferidos en el tiempo (usado principalmente en combate).

*   **`check_and_execute()`**: Se llama en cada ciclo del bucle principal. Comprueba si ha pasado el tiempo estipulado (`interval`) desde la última ejecución y, si es así, ejecuta la función `callback`.
```

### 3. Esquema de Base de Datos (`docs/DATABASE_SCHEMA.md`)

Este archivo explica las tablas SQL utilizadas para definir el mundo.

```diff
# Esquema de Base de Datos (SQLite)

El juego utiliza una base de datos relacional para persistir el mundo y los jugadores.

## Tabla: `players`
Almacena la ficha de los usuarios.
*   **Identificación**: `name`, `password`.
*   **Estado**: `pv` (vida), `e` (energía), `room` (sala actual).
*   **Atributos**: `f` (fuerza), `a` (agilidad), `d` (destreza), etc.
*   **Lore**: `servicio` (facción), `sector`, `clon` (número de vida actual), `traicion` (nivel de búsqueda).
*   **JSON**: `config` (preferencias), `inventario`.

## Tabla: `rooms`
Definición estática de las salas.
*   **`name`**: ID único de texto (ej: "inicio", "lab/farmacia").
*   **`title`**: Nombre visible para el jugador.
*   **`description`**: Texto largo descriptivo.

## Tabla: `exits`
Conexiones entre salas.
*   **`room_name`**: Sala origen.
*   **`exit_name`**: Comando para salir (ej: "norte", "ascensor").
*   **`target_room`**: Sala destino.
*   **`hidden`**: Booleano (0/1) para salidas secretas.

## Tabla: `room_objects`
Objetos decorativos o interactivos en las salas.
*   **`room_name`**: Dónde está.
*   **`object_name`**: Nombre y alias separados por comas (ej: "probeta,probetas").
*   **`description`**: Lo que se ve al hacer "mirar objeto".

## Tabla: `object_interactions`
Define qué pasa al usar un comando sobre un objeto.
*   **`room_name`**, **`object_name`**: Vinculación.
*   **`command`**: Verbo (ej: "beber", "teclear").
*   **`effect`**: Código Python simple a ejecutar (ej: `pv+=10`).
*   **`message`**: Texto a mostrar al jugador tras el éxito.
*   **`cooldown`**: Segundos de espera antes de poder usarlo de nuevo.
*   **`cooldown_message`**: Mensaje si intentas usarlo antes de tiempo.

## Tabla: `npcs`
Personajes no jugadores.
*   **`id`**: Identificador numérico.
*   **`display_name`**: Nombre visible.
*   **`room`**: Ubicación actual.
*   **`pv`, `pv_max`**: Vida.
*   **`f`, `a`, `d`...**: Atributos de combate.
*   **`conversation`**: JSON con árbol de diálogo.
*   **`can_fight`**: Si se le puede atacar.
*   **`respawn_time`**: Tiempo en segundos para revivir.
```

<!--
[PROMPT_SUGGESTION]¿Cómo podría añadir una nueva clase 'Item' para gestionar un inventario real en lugar de usar un diccionario JSON?[/PROMPT_SUGGESTION]
[PROMPT_SUGGESTION]¿Me ayudas a crear un script SQL para añadir una nueva zona de juego llamada 'Sector de Mantenimiento'?[/PROMPT_SUGGESTION]
