import time
import re
from .effect_manager import EffectManager
from .player_manager import PlayerManager  # Ensure PlayerManager is imported

class RoomCommandProcessor:
    def __init__(self, room_manager, players, mud, player_manager):
        self.room_manager = room_manager
        self.players = players
        self.mud = mud
        self.effect_manager = EffectManager(players, mud, player_manager)  # Pass player_manager here

    def process_command(self, id, command, params):
        room = self.room_manager.load_room(self.players[id]["room"])
        if params:  # Si hay parámetros, como "beber probeta azul"
            interaction_key = f"{command} {params}".lower()
            if interaction_key in room["interactions"]:  # Verificar si la interacción existe
                interaction = room["interactions"][interaction_key]
                cooldown = interaction["cooldown"]
                last_used = self.players[id].get("last_used", {}).get(interaction_key, 0)
                current_time = time.time()
                if current_time - last_used < cooldown:
                    remain_time = int(cooldown - (current_time - last_used))
                    if interaction["cooldown_message"]:
                        self.mud.send_message(id, interaction["cooldown_message"].replace("%", str(remain_time)))
                    else:
                        self.mud.send_message(id, f"No puedes {command} en '{params}' aún. Inténtalo en {remain_time} segundos.")
                else:
                    if "last_used" not in self.players[id]:
                        self.players[id]["last_used"] = {}
                    self.players[id]["last_used"][interaction_key] = current_time

                    effect = interaction["effect"]
                    if effect:  # Si hay un efecto asociado, aplicarlo
                        self.effect_manager.apply_effect(id, effect, interaction.get("message"))
                    else:
                        self.mud.send_message(id, "[info] No hay efecto asociado a esta interacción.")
                        self.mud.send_message(id, interaction["message"] if interaction["message"] else "No hay efecto asociado a esta interacción.")
            else:
                self.mud.send_message(id, f"No puedes '{command}' con '{params}'.")
        else:  # Si no hay parámetros, procesar otros comandos dinámicos
            if command in room["exits"]:  # Si el comando es una salida
                self.room_manager.move_player(id, command, self.players, self.mud)
            else:
                self.mud.send_message(id, f"No conozco la orden '{command}' (escribe: ayuda para ver los comandos disponibles).")
                # self.mud.send_message(id, f"No ves ningún '{obj_name}' aquí.")

