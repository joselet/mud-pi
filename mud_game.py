import time
from mudserver import MudServer
from player_manager import PlayerManager
from room_manager import RoomManager
from combat_system import CombatSystem

# Diccionario de alias para las salidas típicas
EXIT_ALIASES = {
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
    "fu": "fuera"
}

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

class MudGame:
    def __init__(self, db_path):
        self.mud = MudServer()
        self.players = {}
        self.player_manager = PlayerManager(db_path)
        self.room_manager = RoomManager(db_path)
        self.combat_system = CombatSystem(self.players, self.mud)

    def run(self):
        while True:
            time.sleep(0.2)
            self.mud.update()
            self.handle_new_players()
            self.handle_disconnected_players()
            self.handle_commands()
            self.combat_system.process_turns()

    def handle_new_players(self):
        for id in self.mud.get_new_players():
            self.players[id] = {"name": None, "room": None, "awaiting_name": True}
            self.mud.send_message(id, "Qué nombre tiene tu personaje?")

    def handle_disconnected_players(self):
        for id in self.mud.get_disconnected_players():
            if id not in self.players:
                continue
            ficha = self.players[id]
            ficha["room"] = self.players[id]["room"]
            self.player_manager.save_player(ficha)
            for pid, pl in self.players.items():
                if pid != id:
                    self.mud.send_message(pid, f"{self.players[id]['display_name']} salió del juego.")
            del self.players[id]

    def handle_commands(self):
        for id, command, params in self.mud.get_commands():
            if id not in self.players:
                continue

            if command in EXIT_ALIASES:
                command = EXIT_ALIASES[command]

            if self.players[id]["awaiting_name"]:
                player_name = command.strip()
                self.players[id]["name"] = player_name
                self.players[id]["awaiting_name"] = False
                self.players[id]["awaiting_password"] = True
                self.players[id]["password_attempts"] = 0
                if self.player_manager.load_player(player_name):
                    self.mud.send_message(id, "Personaje encontrado. Dame la contraseña:")
                else:
                    self.mud.send_message(id, "Personaje no encontrado. Vamos a crearlo. Por favor, establece una contraseña:")
                    self.players[id]["crear_jugador"] = True
            elif self.players[id].get("awaiting_password"):
                try:
                    password = command.strip()
                    if self.players[id].get("crear_jugador"):
                        ficha = self.player_manager.create_player(self.players[id]["name"], password)
                    else:
                        if not self.player_manager.validate_password(self.players[id]["name"], password):
                            raise ValueError("Contraseña incorrecta.")
                        ficha = self.player_manager.load_player(self.players[id]["name"])

                    for pid, pl in self.players.items():
                        if pid != id and pl["name"] == self.players[id]["name"]:
                            self.player_manager.save_player(self.players[pid])
                            self.mud.send_message(pid, "\033[31mEl ordenador ha detectado una suplantación de identidad...\033[0m")
                            self.mud._handle_disconnect(pid)
                            del self.players[pid]
                            break

                    self.players[id].update(ficha)
                    self.players[id]["awaiting_password"] = False
                    self.mud.send_message(id, f"Bienvenido al juego, {self.players[id]['display_name']}. Escribe 'ayuda' para obtener una lista de comandos.")
                    self.room_manager.show_room_to_player(id, self.players, self.mud)
                    for pid, pl in self.players.items():
                        if pid != id:
                            self.mud.send_message(pid, f"[info] {self.players[id]['display_name']} entró al juego.")
                except ValueError as e:
                    self.players[id]["password_attempts"] += 1
                    if self.players[id]["password_attempts"] >= 3:
                        self.mud.send_message(id, "Demasiados intentos fallidos. Desconectando.")
                        print(f"[WRN] El jugador (id: {id}) {self.players[id]['display_name']} se desconectó después de demasiados intentos fallidos en la identificación.")
                        self.mud._handle_disconnect(id)
                        del self.players[id]
                    else:
                        self.mud.send_message(id, f"Error: {e}. Inténtalo de nuevo ({3 - self.players[id]['password_attempts']} intentos restantes).")
            elif command == "ayuda":
                self.mud.send_message(id, "Comandos básicos:")
                self.mud.send_message(id, "  decir <message>  - Decir algo en voz alta")
                self.mud.send_message(id, "  mirar            - Examina tu alrededor")
                self.mud.send_message(id, "  ir <exit>        - Mover hacia la salida especificada")
                self.mud.send_message(id, "  estado           - Comprobar la ficha y estado de tu personaje")
                self.mud.send_message(id, "  matar <objetivo> - Atacar a otro personaje")
                self.mud.send_message(id, "  abandonar        - Abandonar el juego")
            elif command == "decir":
                for pid, pl in self.players.items():
                    if self.players[pid]["room"] == self.players[id]["room"]:
                        self.mud.send_message(pid, f"{self.players[id]['display_name']} dice: {params}")
            elif command == "mirar":
                self.room_manager.show_room_to_player(id, self.players, self.mud)
            elif command == "ir":
                self.room_manager.move_player(id, params, self.players, self.mud)
            elif command == "abandonar":
                self.mud.send_message(id, "Desconectando. Adiós!")
                ficha = self.players[id]
                ficha["room"] = self.players[id]["room"]
                self.player_manager.save_player(ficha)
                for pid, pl in self.players.items():
                    if pid != id:
                        self.mud.send_message(pid, f"[info] {self.players[id]['name']} se marchó del juego.")
                self.mud._handle_disconnect(id)
                if id in self.players:
                    del self.players[id]
            elif command == "estado":
                ficha = self.players[id]
                self.mud.send_message(id, (
                    f"Eres {ficha['display_name']}, agente esclarecedor con Código de Seguridad:{NIVEL_COLOR.get(ficha.get('nivel', 0))} {NIVEL_DISPLAY.get(ficha.get('nivel', 0))} {NIVEL_COLOR.get('reset')} y clonado {ficha.get('clon', 1)} veces:\n"
                    f"Te han asignado al servicio: {ficha.get('servicio', 'Ninguno')}\n"
                    f"Perteneces a la sociedad secreta: {ficha.get('sociedad_secreta', 'Ninguna')}\n"
                    f"Vives en el sector: {ficha.get('sector', 'Desconocido')}\n"
                    f"  Vida (pv): {ficha.get('pv', 0)}\n"
                    f"  Energía (e): {ficha.get('e', 0)}\n"
                    f"  Fuerza (f): {ficha.get('f', 0)}\n"
                    f"  Resistencia (r): {ficha.get('r', 0)}\n"
                    f"  Agilidad (a): {ficha.get('a', 0)}\n"
                    f"  Destreza (d): {ficha.get('d', 0)}\n"
                    f"  Percepción (p): {ficha.get('p', 0)}\n"
                    f"  Cinismo (c): {ficha.get('c', 0)}\n"
                    f"  Talento mecánico (tm): {ficha.get('tm', 0)}\n"
                    f"  Poder mutante (pm): {ficha.get('pm', 0)}\n"
                    f"  Sala actual: {ficha.get('room', 'Desconocida')}"
                ))
            elif command == "matar":
                self.combat_system.start_combat(id, params)
            else:
                try:
                    room = self.room_manager.load_room(self.players[id]["room"])
                    if command in room["exits"]:
                        self.room_manager.move_player(id, command, self.players, self.mud)
                    else:
                        self.mud.send_message(id, f"No conozco la orden '{command}' (escribe: ayuda para ver los comandos disponibles)")
                except ValueError as e:
                    self.mud.send_message(id, "\033[31mHas sufrido un fallo espacio/tiempo y apareces en la incubadora.\033[0m")
                    self.players[id]["room"] = "respawn"
                    self.room_manager.show_room_to_player(id, self.players, self.mud)
