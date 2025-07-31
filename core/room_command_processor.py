import time
import re

class RoomCommandProcessor:
    def __init__(self, room_manager, players, mud):
        self.room_manager = room_manager
        self.players = players
        self.mud = mud

    def process_command(self, id, command, params):
        room = self.room_manager.load_room(self.players[id]["room"])
        if params:  # Si hay parámetros, como "beber fuente"
            obj_name = params.lower()
            if obj_name in room["objects"]:
                obj = room["objects"][obj_name]
                if command in obj["interactions"]:  # Verificar si el comando está asociado al objeto
                    interaction = obj["interactions"][command]
                    cooldown = interaction["cooldown"]
                    last_used = self.players[id].get("last_used", {}).get(obj_name, {}).get(command, 0)
                    current_time = time.time()
                    if current_time - last_used < cooldown:
                        remain_time = int(cooldown - (current_time - last_used))
                        if interaction["cooldown_message"]:
                            self.mud.send_message(id, interaction["cooldown_message"].replace("%", str(remain_time)))
                        else:
                            self.mud.send_message(id, f"No puedes {command} en '{obj_name}' aún. Inténtalo en {remain_time} segundos.")
                    else:
                        if "last_used" not in self.players[id]:
                            self.players[id]["last_used"] = {}
                        if obj_name not in self.players[id]["last_used"]:
                            self.players[id]["last_used"][obj_name] = {}
                        self.players[id]["last_used"][obj_name][command] = current_time

                        effect = interaction["effect"]
                        if effect:
                            match = re.match(r"(\w+)([+\-=])(\d+)", effect)
                            if match:
                                key, operator, value = match.groups()
                                value = int(value)

                                if key == "energia":
                                    if operator == "+":
                                        self.players[id]["e"] = min(self.players[id].get("e", 0) + value, 100)
                                        self.mud.send_message(id, f"[info] Recuperas {value} puntos de energía.")
                                    elif operator == "-":
                                        self.players[id]["e"] = max(self.players[id].get("e", 0) - value, 0)
                                        self.mud.send_message(id, f"[info] Pierdes {value} puntos de energía.")
                                    elif operator == "=":
                                        self.players[id]["e"] = min(max(value, 0), 100)
                                        self.mud.send_message(id, f"[info] Tu energía se establece en {value}.")
                                else:
                                    self.mud.send_message(id, f"[info] El efecto '{effect}' no está implementado.")
                            else:
                                self.mud.send_message(id, f"[info] Formato de efecto inválido: '{effect}'.")
                        else:
                            self.mud.send_message(id, "[info] No hay efecto asociado a esta interacción.")

                        if interaction["message"]:
                            self.mud.send_message(id, interaction["message"])
                else:
                    self.mud.send_message(id, f"No puedes '{command}' con {obj_name}.")
            else:
                self.mud.send_message(id, f"No ves ningún '{obj_name}' aquí.")
        else:  # Si no hay parámetros, procesar otros comandos dinámicos
            if command in room["exits"]:  # Si el comando es una salida
                self.room_manager.move_player(id, command, self.players, self.mud)
            else:
                self.mud.send_message(id, f"No conozco la orden '{command}' (escribe: ayuda para ver los comandos disponibles).")
