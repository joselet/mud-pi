# Documentación del Proyecto MUD-Pi (Paranoia)

Este proyecto es un motor de juego MUD (Multi-User Dungeon) basado en texto, ambientado en el universo de **Paranoia** (El Ordenador, el Complejo Alfa, clones, traiciones, etc.).

El sistema utiliza una arquitectura cliente-servidor mediante Sockets TCP/IP (Telnet) y almacena el estado del mundo y los jugadores en una base de datos SQLite.

## Estructura de Archivos

### Raíz del Proyecto
*   **`paranoia.py`**: Punto de entrada principal del servidor. Inicializa el juego y comienza el bucle principal.
*   **`client.py`**: Un cliente Telnet básico escrito en Python para conectarse al servidor.

### Directorio `core/` (El Motor)
Aquí reside la lógica del juego.

*   **`mud_game.py`**: La clase principal que orquesta todo ("El Dios" del juego).
*   **`mudserver.py`**: Manejo de bajo nivel de sockets y protocolo Telnet.
*   **`player_manager.py`**: Gestión de fichas de personajes y base de datos de jugadores.
*   **`room_manager.py`**: Gestión de habitaciones, movimiento y carga desde BD.
*   **`combat_system.py`**: Lógica de combate por turnos (PvP y PvE).
*   **`effect_manager.py`**: Sistema para aplicar efectos dinámicos (curación, daño, etc.).
*   **`room_command_processor.py`**: Procesa comandos específicos de objetos en las habitaciones.
*   **`npc_manager.py`**: Utilidades para NPCs (como el respawn).
*   **`timer.py`**: Utilidad para ejecutar código con retardo (usado en combate).
*   **`config.py`**: Constantes, colores ANSI, textos de ambientación y alias de comandos.

### Directorio `data/`
*   **`mud.db`**: Base de datos SQLite (se crea/actualiza con los scripts SQL).

### Directorio `admin/`
*   **`*.sql`**: Scripts para poblar la base de datos (habitaciones, objetos, NPCs).

## Flujo de Ejecución

1.  Se ejecuta `paranoia.py`.
2.  Se instancia `MudGame`.
3.  `MudGame` inicializa el servidor (`MudServer`) y los gestores (`PlayerManager`, `RoomManager`, etc.).
4.  Entra en un bucle infinito (`run()`) que:
    *   Actualiza la red (`mud.update()`).
    *   Gestiona nuevos jugadores (`handle_new_players`).
    *   Procesa comandos de texto (`handle_commands`).
    *   Procesa turnos de combate (`combat_system.process_turns`).
    *   Duerme brevemente para no saturar la CPU.

Para más detalles técnicos, consulta `CORE_REFERENCE.md`.
Para detalles sobre los datos, consulta `DATABASE_SCHEMA.md`.