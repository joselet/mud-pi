import random
from .timer import Timer

class CombatSystem:
    def __init__(self, players, mud):
        self.players = players
        self.mud = mud
        self.active_combats = {}

    def start_combat(self, attacker_id, victim_name):
        victim_name = victim_name.strip().lower()
        victim_id = None
        for pid, pl in self.players.items():
            if pl["name"].strip().lower() == victim_name and self.players[pid]["room"] == self.players[attacker_id]["room"]:
                victim_id = pid
                break

        if victim_id is None:
            self.mud.send_message(attacker_id, f"No se encontró al jugador '{victim_name}' en esta sala.")
            return

        if attacker_id in self.active_combats or victim_id in self.active_combats:
            self.mud.send_message(attacker_id, "Ya estás en un combate.")
            return

        self.active_combats[attacker_id] = {
            "victim": victim_id,
            "turn": attacker_id,
            "timer": Timer(2, lambda: self.process_turn(attacker_id))
        }
        self.active_combats[victim_id] = {
            "victim": attacker_id,
            "turn": attacker_id,
            "timer": None
        }

        self.mud.send_message(attacker_id, f"Has iniciado un combate contra {self.players[victim_id]['display_name']}.")
        self.mud.send_message(victim_id, f"{self.players[attacker_id]['display_name']} te ha atacado. ¡Prepárate para luchar!")

        # Realizar el primer ataque instantáneamente
        self.process_turn(attacker_id)

    def process_turns(self):
        for attacker_id, combat in list(self.active_combats.items()):
            if combat["timer"]:
                combat["timer"].check_and_execute()

    def process_turn(self, attacker_id):
        combat = self.active_combats.get(attacker_id)
        if not combat:
            return

        victim_id = combat["victim"]
        attacker = self.players[attacker_id]
        victim = self.players[victim_id]

        if attacker["room"] != victim["room"]:
            self.mud.send_message(attacker_id, f"El combate con {victim['display_name']} ha terminado porque ya no están en la misma sala.")
            self.mud.send_message(victim_id, f"El combate con {attacker['display_name']} ha terminado porque ya no están en la misma sala.")
            del self.active_combats[attacker_id]
            del self.active_combats[victim_id]
            return

        if attacker["e"] <= 0:
            self.mud.send_message(attacker_id, "No tienes suficiente energía para atacar.")
            self.mud.send_message(victim_id, f"{attacker['display_name']} Realiza un penoso gesto de ataque, pero agotado desfallece en el intento.")
            combat["turn"] = victim_id
        else:
            roll = random.randint(0, 5)
            damage = max(0, attacker["f"] + roll - victim["r"])
            victim["pv"] -= damage
            attacker["e"] -= 1

            self.mud.send_message(attacker_id, f"Tirada: {attacker['f']} (Fue.A) + {roll} - {victim['r']} (Res.R) = {damage} -> Has infligido {damage} de daño a {victim['display_name']}.")
            self.mud.send_message(victim_id, f"Tirada: {attacker['f']} (Fue.A) + {roll} - {victim['r']} (Res.R) = {damage} -> Has recibido {damage} de daño de {attacker['display_name']}. Puntos de vida restantes: {victim['pv']}")

            if victim["pv"] <= 0:
                self.end_combat(attacker_id, victim_id)
                return

        combat["turn"] = victim_id
        if self.active_combats[victim_id]:
            self.active_combats[victim_id]["timer"] = Timer(2, lambda: self.process_turn(victim_id))

        # if victim["e"] > 0:
        #     response_roll = random.randint(0, 5)
        #     response_damage = max(0, victim["f"] + response_roll - attacker["r"])
        #     attacker["pv"] -= response_damage
        #     victim["e"] -= 1

        #     self.mud.send_message(victim_id, f"Tirada: {victim['f']} (Fue.V) + {response_roll} - {attacker['r']} (Res.A) = {response_damage} -> En respuesta, Has infligido {response_damage} de daño a {attacker['display_name']}.")
        #     self.mud.send_message(attacker_id, f"Tirada: {victim['f']} (Fue.V) + {response_roll} - {attacker['r']} (Res.A) = {response_damage} -> En respuesta, Has recibido {response_damage} de daño de {victim['display_name']}. Puntos de vida restantes: {attacker['pv']}")

        #     if attacker["pv"] <= 0:
        #         self.end_combat(victim_id, attacker_id)
        #         return
        # else:
        #     self.mud.send_message(victim_id, "No tienes suficiente energía para contraatacar.")
        #     self.mud.send_message(attacker_id, f"{victim['display_name']} Realiza un penoso gesto de ataque, pero agotado desfallece en el intento.")

        combat["timer"] = None

    def end_combat(self, winner_id, loser_id):
        del self.active_combats[winner_id]
        del self.active_combats[loser_id]

        self.mud.send_message(winner_id, f"\033[93m¡Has derrotado a {self.players[loser_id]['display_name']}!\033[0m")
        self.mud.send_message(loser_id, f"\033[31m¡Has sido derrotado por {self.players[winner_id]['display_name']}!\033[0m")
        self.mud.send_message(loser_id, f"\033[93mDebido a tu pobre genética, las celulas de tu cuerpo se deshacen lentamente debido a la falta de irrigación mantenida por tu bomba de fluido sanguíneo.\nPor imperativa del ordenador, los restos de tu triste cuerpo son trasladados a la planta de regeneración para ser reciclados y finalmene formar una nueva vida.\nTu alma y tu psique es transferida a un nuevo cuerpo.\033[0m")

        for pid, pl in self.players.items():
            if pid != loser_id:
                self.mud.send_message(pid, f"[info] {self.players[loser_id]['name']} ha muerto.")

        self.players[loser_id]["room"] = "respawn"
        self.players[loser_id]["clon"] += 1
        self.players[loser_id]["display_name"] = f"{self.players[loser_id]['name'].capitalize()}-{self.players[loser_id]['sector']}-{self.players[loser_id]['clon']}"
        self.players[loser_id]["pv"] = 25
