import re

class EffectManager:
    def __init__(self, players, mud, player_manager):
        self.players = players
        self.mud = mud
        self.player_manager = player_manager  # Nuevo parámetro para manejar jugadores


    # función para aplicar efectos (una propuesta mas segura que hacer eval(effect))
    def apply_effect(self, player_id, effect, message=None):
        """
        Aplica un efecto al jugador basado en una expresión almacenada en la base de datos.
        :param player_id: ID del jugador al que se aplica el efecto.
        :param effect: Expresión que modifica los atributos del jugador (e.g., "pv += 10").
        :param message: Mensaje opcional que se envía al jugador.
        """
        if player_id not in self.players:
            self.mud.send_message(player_id, "[error] Jugador no encontrado.")
            return

        # Crear un contexto seguro con las variables del jugador
        context = {
            "pv": self.players[player_id].get("pv", 0),
            "e": self.players[player_id].get("e", 0),
        }

        # Agregar dinámicamente todas las claves del jugador al contexto
        for key, value in self.players[player_id].items():
            if key not in context:
                context[key] = value

        try:
            # Ejecutar la expresión en el contexto
            exec(effect, {"__builtins__": None}, context)

            # Actualizar los valores del jugador
            for key in context:
                if key in self.players[player_id]:
                    self.players[player_id][key] = context[key]
                else:
                    # Si es una nueva clave, inicializarla
                    self.players[player_id][key] = context[key]
            
            # grabar ficha en la base de datos
            self.player_manager.save_player(self.players[player_id])  # Cambiado a self.player_manager

            # Enviar mensajes al jugador (DEBUG)
            self.mud.send_message(player_id, f"[info] Se aplicó {effect}.")
            # for key in context:
            #     self.mud.send_message(player_id, f"[info] {key}: {context[key]}")

            if message:
                self.mud.send_message(player_id, message)

        except Exception as e:
            self.mud.send_message(player_id, f"[error] Error al aplicar el efecto: {e}")

    # def apply_effect(self, player_id, effect, message=None):
    #     """
    #     Aplica un efecto a un jugador.
    #     :param player_id: ID del jugador al que se aplica el efecto.
    #     :param effect: Cadena con el efecto (e.g., "energia+10", "vida-5").
    #     :param message: Mensaje opcional que se envía al jugador.
    #     """
    #     if not effect:
    #         return

    #     match = re.match(r"(\w+)([+\-=])(\d+)", effect)
    #     if not match:
    #         self.mud.send_message(player_id, f"[info] Formato de efecto inválido: '{effect}'.")
    #         return

    #     key, operator, value = match.groups()
    #     value = int(value)

    #     if key in ["energia", "e"]:
    #         if operator == "+":
    #             self.players[player_id]["e"] = min(self.players[player_id].get("e", 0) + value, 100)
    #         elif operator == "-":
    #             self.players[player_id]["e"] = max(self.players[player_id].get("e", 0) - value, 0)
    #         elif operator == "=":
    #             self.players[player_id]["e"] = min(max(value, 0), 100)
    #         self.mud.send_message(player_id, f"[info] Tu energía ahora es {self.players[player_id]['e'].}")

    #     elif key in ["vida", "pv"]:
    #         if operator == "+":
    #             self.players[player_id]["pv"] = min(self.players[player_id].get("pv", 0) + value, 100)
    #         elif operator == "-":
    #             self.players[player_id]["pv"] = max(self.players[player_id].get("pv", 0) - value, 0)
    #         elif operator == "=":
    #             self.players[player_id]["pv"] = min(max(value, 0), 100)
    #         self.mud.send_message(player_id, f"[info] Tu vida ahora es {self.players[player_id]['pv']}.")

    #     else:
    #         self.mud.send_message(player_id, f"[info] El efecto '{effect}' no está implementado.")

    #     if message:
    #         self.mud.send_message(player_id, message)
