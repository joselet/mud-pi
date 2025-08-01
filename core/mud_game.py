import time
# import re # For regex operations (en efectos de objetos, para buscar el operador)
from .mudserver import MudServer
from .player_manager import PlayerManager
from .room_manager import RoomManager
from .combat_system import CombatSystem
from .config import NIVEL_DISPLAY, NIVEL_COLOR, COMMAND_ALIASES, SERVICIOS
from .room_command_processor import RoomCommandProcessor


class MudGame:
    def __init__(self, db_path):
        self.mud = MudServer()
        self.players = {}
        self.player_manager = PlayerManager(db_path)
        self.room_manager = RoomManager(db_path)
        self.combat_system = CombatSystem(self.players, self.mud)
        self.room_command_processor = RoomCommandProcessor(self.room_manager, self.players, self.mud)

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
            print(f"[LOG] (pid: {id}) {self.players[id]['name']} se desconectó de forma forzada.")
            for pid, pl in self.players.items():
                if pid != id:
                    if self.players[id]['name']:
                        self.mud.send_message(pid, f"{self.players[id]['name']} salió del juego.")
                    else:
                        self.mud.send_message(pid, f"Jugador (id: {id}) salió del juego.")
            del self.players[id]

    def handle_commands(self):
        for id, command, params in self.mud.get_commands():
            if id not in self.players:
                continue

            if self.players[id]["awaiting_name"]:
                player_name = command.strip()
                if not player_name:
                    self.mud.send_message(id, "El nombre no puede estar vacío. Por favor, inténtalo de nuevo.")
                    return
                if len(player_name) < 3 or len(player_name) > 20:
                    self.mud.send_message(id, "El nombre debe tener entre 3 y 20 caracteres. Por favor, inténtalo de nuevo.")
                    return
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
                            self.mud.send_message(pid, "\033[31mEl ordenador ha detectado una suplantación de identidad y ha decidido desconectar tu sistema neurológico por seguridad. Tu alma es expulsada y se transfiere a un banco de datos fuera de tu control para investigar la anomalía. Tu cuerpo recibe una consciencia validada por el sistema informático central del ordenador.\nDe ahora en adelante, estarás vigilado.\033[0m")
                            print(f"[WRN] El jugador (id: {id}) coincide con (id: {pid}) {self.players[id]['name']} se desconecta y se deja paso a la nueva conexión: ({id}).")
                            self.mud._handle_disconnect(pid)
                            del self.players[pid]
                            break

                    self.players[id].update(ficha)
                    self.players[id]["awaiting_password"] = False
                    self.mud.send_message(id, f"Bienvenido al juego, {self.players[id]['display_name']}. Escribe 'ayuda' para obtener una lista de comandos.")
                    print(f"[LOG] (pid: {id}) {self.players[id]['name']} entró al juego.")
                    self.room_manager.show_room_to_player(id, self.players, self.mud)
                    # notificar a otros jugadores
                    for pid, pl in self.players.items():
                        if pid != id:
                            self.mud.send_message(pid, f"[info] {self.players[id]['display_name']} entró al juego.")
                    # notificar a los jugadores de la sala actual que acabas de aparecer en esta sala
                    for pid, pl in self.players.items():
                        if self.players[pid]["room"] == self.players[id]["room"] and pid != id:
                            self.mud.send_message(pid, f"{self.players[id]['display_name']} acaba de aparecer aquí por arte de magia.")
                except ValueError as e:
                    self.players[id]["password_attempts"] += 1
                    if self.players[id]["password_attempts"] >= 3:
                        self.mud.send_message(id, "Demasiados intentos fallidos. Desconectando.")
                        print(f"[WRN] El jugador (id: {id}) {self.players[id]['name']} se desconectó después de demasiados intentos fallidos en la identificación.")
                        self.mud._handle_disconnect(id)
                        del self.players[id]
                    else:
                        self.mud.send_message(id, f"Error: {e}. Inténtalo de nuevo ({3 - self.players[id]['password_attempts']} intentos restantes).")
            else:
                if command in COMMAND_ALIASES:
                    command = COMMAND_ALIASES[command]

                if command == "ayuda":
                    self.mud.send_message(id, "Comandos básicos:")
                    self.mud.send_message(id, "  decir <message>  - Decir algo en voz alta")
                    self.mud.send_message(id, "  mirar            - Examina tu alrededor")
                    self.mud.send_message(id, "  ir <exit>        - Mover hacia la salida especificada")
                    self.mud.send_message(id, "  ficha            - Comprobar la ficha y estado de tu personaje")
                    self.mud.send_message(id, "  matar <objetivo> - Atacar a otro personaje")
                    self.mud.send_message(id, "  config           - configura algun aspecto del juego y tu personaje (en desarrollo)")
                    self.mud.send_message(id, "  abandonar        - Abandonar el juego")
                elif command == "decir":
                    for pid, pl in self.players.items():
                        if self.players[pid]["room"] == self.players[id]["room"]:
                            self.mud.send_message(pid, f"{self.players[id]['display_name']} dice: {params}")
                elif command == "mirar":
                    room = self.room_manager.load_room(self.players[id]["room"])
                    if params:  # Si se especifica un objeto
                        obj_name = params.lower()
                        # Buscar si el objeto o alguno de sus alias está en la sala
                        matching_object = next(
                            (obj for alias, obj in room["objects"].items() if obj_name in alias.split(",")),
                            None
                        )
                        if matching_object:
                            self.mud.send_message(id, matching_object["description"])
                        else:
                            self.mud.send_message(id, f"No ves ningún '{obj_name}' aquí.")
                    else:  # Si no se especifica un objeto, mostrar la sala
                        # recuperar la configuración detallada del jugador
                        config_detallado_actual = self.players[id].get("config_detallado", True)
                        # forzar la visualización detallada
                        self.players[id]["config_detallado"] = True
                        self.room_manager.show_room_to_player(id, self.players, self.mud)
                        # restaurar la configuración detallada del jugador
                        self.players[id]["config_detallado"] = config_detallado_actual
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
                    print(f"[LOG] (pid: {id}) {self.players[id]['name']} se desconectó.")
                    self.mud._handle_disconnect(id)
                    if id in self.players:
                        del self.players[id]
                elif command == "ficha":
                    ficha = self.players[id]
                    if params:
                        if params.lower() == "servicio":
                            if ficha.get("nivel", 0) < 1:
                                self.mud.send_message(id, "No tienes acceso a información de servicios. Tu código de seguridad es demasiado bajo.")
                                self.mud.send_message(id, f"Pretender obtener información por encima de tu CS está perseguido por '{NIVEL_COLOR.get(8)}el Ordenador{NIVEL_COLOR.get('reset')}'.")
                                ficha["traicion"] += 1
                                print(f"[LOG] Jugador (id= {id}) {ficha['name']} Intento de acceso a información de servicio sin autorización. Traición incrementada.")
                                self.player_manager.save_player(ficha)
                                self.mud.send_message(id, f"Tu nivel de traición ha aumentado a {ficha.get('traicion', 0)}. Si llegas a 10, serás vaporizado por orden del ordenador.")
                            if ficha.get("nivel",0) > 0:
                                self.mud.send_message(id, f"Acceso con CS '{NIVEL_COLOR.get(ficha.get('nivel', 0))}{NIVEL_DISPLAY.get(ficha.get('nivel', 0))}{NIVEL_COLOR.get('reset')}' a información del servicio {ficha.get('servicio')}:\n"
                                    f"{SERVICIOS.get(ficha.get('servicio'), {}).get('titulo', 'No hay información disponible.')}")
                            if ficha.get("nivel", 0) > 1:      
                                self.mud.send_message(id,f"{SERVICIOS.get(ficha.get('servicio'), {}).get('descripcion', 'No hay información disponible.')}")
                        else:
                            self.mud.send_message(id, f"Que pretendes obtener con 'ficha {params.lower()}'? Extraer infomación no autorizada está penada por el Código Penal del Complejo Alfa. Si quieres ver tu ficha, escribe 'ficha' a secas.")  
                    else:
                        self.mud.send_message(id, (
                            f"Eres {ficha['display_name']}, agente esclarecedor con Código de Seguridad: {NIVEL_COLOR.get(ficha.get('nivel', 0))}{NIVEL_DISPLAY.get(ficha.get('nivel', 0))}{NIVEL_COLOR.get('reset')} y clonado {ficha.get('clon', 1)} veces:\n"
                            f"Te han asignado al servicio: {ficha.get('servicio', 'Ninguno')}\n"
                            f"Perteneces a la sociedad secreta: {ficha.get('sociedad_secreta', 'Ninguna')}\n"
                            f"Vives en el sector: {ficha.get('sector', 'Desconocido')}\n"
                            f"  {NIVEL_COLOR.get(8)}Puntos de TRAICIóN: {ficha.get('traicion', 0)}{NIVEL_COLOR.get('reset')}\n"
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
                            f"  Sala actual: {ficha.get('room', 'Desconocida')}\n\n"
                            f"Otros parámetros para 'ficha <parametro>': {NIVEL_COLOR.get(1)}servicio{NIVEL_COLOR.get('reset')}"
                        ))
                elif command == "matar":
                    self.combat_system.start_combat(id, params)
                elif command == "config":
                    if params:
                        if params.lower() == "detallado off":
                            self.players[id]["config"]["detallado"] = False
                            self.mud.send_message(id, "Modo detallado desactivado. Usa 'mirar' para ver el detalle de las rooms.")
                        elif params.lower() == "detallado on":
                            self.players[id]["config"]["detallado"] = True
                            self.mud.send_message(id, "Modo detallado activado. Verás más detalles al entrar en un lugar.")
                        elif params.lower() == "tiradas off":
                            self.players[id]["config"]["tiradas"] = False
                            self.mud.send_message(id, "Visualización de tiradas de dados desactivada.")
                        elif params.lower() == "tiradas on":
                            self.players[id]["config"]["tiradas"] = True
                            self.mud.send_message(id, "Visualización de tiradas de dados activada.")
                        else:
                            self.mud.send_message(id, f"Comando 'config {params.lower()}' no reconocido. Teclea 'config' para ver la sintaxis.")
                    else:
                        self.mud.send_message(id, 
                            f"Ayuda del comando config:\n"
                            "  config <opción> <valor> - Configura una opción del juego o del personaje\n"
                            "Opciones disponibles:\n"
                            "  - tiradas [on/off]: Activa o desactiva la visualización de las tiradas de dados\n"
                            "  - detallado [on/off]: Cambia el nivel de detalle de los lugares que visites (para ver el detalle siempre puedes 'mirar' el lugar)\n"
                            "Tu configuración actual:\n"
                            f"  - tiradas: {'on' if self.players[id]['config'].get('tiradas', False) else 'off'}\n"
                            f"  - detallado: {'on' if self.players[id]['config'].get('detallado', True) else 'off'}\n"
                        )
                else:
                    try: ## procesar comandos dinámicos, salidas, alias y objetos e interacciones
                        self.room_command_processor.process_command(id, command, params)
                    except ValueError as e:
                        self.mud.send_message(id, "\033[31mHas sufrido un fallo espacio/tiempo y apareces en la incubadora.\033[0m")
                        print(f"[ERR] Fallo para (pid= {id}). Comando: {command} (Error: {e})")
                        self.players[id]["room"] = "respawn"
                        self.room_manager.show_room_to_player(id, self.players, self.mud)
