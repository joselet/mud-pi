import random
from .timer import Timer
from .room_manager import RoomManager

class CombatSystem:
    def __init__(self, players, mud, room_manager):
        self.players = players
        self.mud = mud
        self.room_manager = room_manager
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
        #loguear
        print(f"[LOG] (Ataque a jugadores) Attacker ID: {attacker_id}, Victim ID: {victim_id}")
        # para qué esta info? print(f"[LOG]NPCs in room: {[npc['id'] for npc in self.room_manager.load_npcs_in_room(self.players[attacker_id]['room'])]}")

        # Realizar el primer ataque instantáneamente
        self.process_turn(attacker_id)


    def start_combat_with_npc(self, player_id, npc):
        if player_id in self.active_combats:
            self.mud.send_message(player_id, "Ya estás en un combate.")
            return

        self.active_combats[player_id] = {
            "victim": npc["id"],
            "turn": player_id,
            "timer": Timer(2, lambda: self.process_turn(player_id))
        }
        self.mud.send_message(player_id, f"Has iniciado un combate contra {npc['display_name']}.")
        #loguear
        print(f"[LOG] (Ataque a NPC) Attacker ID: {player_id}, NPC ID: {npc['id']}")
        print(f"[LOG] NPCs in room: {[npc['id'] for npc in self.room_manager.load_npcs_in_room(self.players[player_id]['room'])]}")
        self.process_turn(player_id)



    # funcion llamada por mud_game. Quizas para gestionar si toca ya ejecutar un turno?
    def process_turns(self):
        for attacker_id, combat in list(self.active_combats.items()):
            if combat["timer"]:
                combat["timer"].check_and_execute()

    def process_turn(self, attacker_id):
        combat = self.active_combats.get(attacker_id)
        if not combat:
            print (f"[LOG-debug] No combat found for attacker ID: {attacker_id}")
            return

        victim_id = combat["victim"]
        attacker = self.players.get(attacker_id, None)
        print (f"[LOG-debug] Process turn for attacker ID: {attacker_id}, Victim ID: {victim_id}")
        # Determinar si la víctima es un NPC (_npc0,_npc1,..) o un jugador (0,1,2,..)
        if str(victim_id).startswith("_npc"):
            victim_is_npc = True
            victim = next(
                (npc for npc in self.room_manager.load_npcs_in_room(attacker["room"]) if npc["id"] == victim_id),
                None
            )
            if not victim:
                # Si el NPC ya no está en la sala, termina el combate
                self.mud.send_message(attacker_id, f"El combate con el NPC ha terminado porque ya no está en la sala.")
                del self.active_combats[attacker_id]
                return
        else:
            victim_is_npc = False
            victim = self.players.get(victim_id, None)
            if not victim:
                # Si el jugador ya no está disponible, termina el combate
                self.mud.send_message(attacker_id, f"El combate con el jugador ha terminado porque ya no está disponible.")
                del self.active_combats[attacker_id]
                return

        # Verificar si están en la misma sala
        if attacker["room"] != victim["room"]:
            self.mud.send_message(attacker_id, f"El combate con {victim['display_name']} ha terminado porque ya no están en la misma sala.")
            if not victim_is_npc:
                self.mud.send_message(victim_id, f"El combate con {attacker['display_name']} ha terminado porque ya no están en la misma sala.")
            del self.active_combats[attacker_id]
            if not victim_is_npc:
                del self.active_combats[victim_id]
            return

        # Verificar si el atacante tiene suficiente energía (solo jugadores)
        if attacker["e"] <= 0:
            self.mud.send_message(attacker_id, "No tienes suficiente energía para atacar.")
            if not victim_is_npc:
                self.mud.send_message(victim_id, f"{attacker['display_name']} intenta atacarte, pero está demasiado agotado.")
            combat["turn"] = victim_id
            return

        # Realizar la tirada de agilidad para determinar si el ataque tiene éxito
        rolla = random.randint(0, 5)
        rollv = random.randint(0, 5)
        chance = attacker["d"] + rolla - victim["a"] - rollv

        # Mensajes de tiradas si están activados
        if attacker_id in self.players and self.players[attacker_id]["config"].get("tiradas", False):
            self.mud.send_message(attacker_id, f"[info] Tirada Dest vs Agil: {attacker['d']} (Dest.A) + {rolla} - {victim['a']} (Agil.V) + {rollv} = {chance}")
        if not victim_is_npc and victim["config"].get("tiradas", False):
            self.mud.send_message(victim_id, f"[info] Tirada Dest vs Agil: {attacker['d']} (Dest.A) + {rolla} - {victim['a']} (Agil.V) + {rollv} = {chance}")

        if chance < 0:
            # El ataque falla
            self.mud.send_message(attacker_id, f"Tu ataque contra {victim['display_name']} ha fallado.")
            if not victim_is_npc:
                self.mud.send_message(victim_id, f"Has esquivado el ataque de {attacker['display_name']}.")
        else:
            # El ataque tiene éxito, calcular daño
            roll = random.randint(0, 5)
            damage = max(0, attacker["f"] + roll - victim["r"])
            victim["pv"] -= damage
            #if not attacker_id.startswith("_npc"):
            attacker["e"] -= 1  # Reducir energía del atacante (~~solo jugadores~~ jugadores y npc)

            # Mensajes de daño
            self.mud.send_message(attacker_id, f"Has infligido {damage} de daño a {victim['display_name']}.")
            if not victim_is_npc:
                self.mud.send_message(victim_id, f"Has recibido {damage} de daño de {attacker['display_name']}. Puntos de vida restantes: {victim['pv']}")

            # Verificar si la víctima ha muerto
            if victim["pv"] <= 0:
                if victim_is_npc:
                    self.mud.send_message(attacker_id, f"¡Has derrotado a {victim['display_name']}!")
                    del self.active_combats[attacker_id]
                else:
                    self.end_combat(attacker_id, victim_id)
                return

        # Cambiar el turno
        combat["turn"] = victim_id
        if not victim_is_npc and self.active_combats[victim_id]:
            self.active_combats[victim_id]["timer"] = Timer(2, lambda: self.process_turn(victim_id))
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
