import random
from .timer import Timer
from .room_manager import RoomManager
from .effect_manager import EffectManager
from .player_manager import PlayerManager  # Ensure PlayerManager is imported

class CombatSystem:
    def __init__(self, game):
        self.game = game
        self.effect_manager = EffectManager(game)
        self.active_combats = {}

    def start_combat(self, attacker_id, victim_name):
        victim_name = victim_name.strip().lower()
        victim_id = None
        for pid, pl in self.game.players.items():
            if pl["name"].strip().lower() == victim_name and self.game.players[pid]["room"] == self.game.players[attacker_id]["room"]:
                victim_id = pid
                break

        if victim_id is None:
            self.game.mud.send_message(attacker_id, f"No se encontró al jugador '{victim_name}' en esta sala.")
            return

        if attacker_id in self.active_combats or victim_id in self.active_combats:
            self.game.mud.send_message(attacker_id, "Ya estás en un combate.")
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

        self.game.mud.send_message(attacker_id, f"Has iniciado un combate contra {self.game.players[victim_id]['display_name']}.")
        self.game.mud.send_message(victim_id, f"{self.game.players[attacker_id]['display_name']} te ha atacado. ¡Prepárate para luchar!")
        #loguear
        print(f"[LOG] (Ataque a jugadores) Attacker ID: {attacker_id}, Victim ID: {victim_id}")
        # para qué esta info? print(f"[LOG]NPCs in room: {[npc['id'] for npc in self.room_manager.load_npcs_in_room(self.players[attacker_id]['room'])]}")

        # Realizar el primer ataque instantáneamente
        self.process_turn(attacker_id)


    def start_combat_with_npc(self, player_id, npc):
        if player_id in self.active_combats:
            self.game.mud.send_message(player_id, "Ya estás en un combate.")
            return

        self.active_combats[player_id] = {
            "victim": npc["id"],
            "turn": player_id,
            "timer": Timer(2, lambda: self.process_turn(player_id))
        }
        self.game.mud.send_message(player_id, f"Has iniciado un combate contra {npc['display_name']}.")
        #loguear
        print(f"[LOG] (Ataque a NPC) ID atacante: {player_id}, NPC ID: {npc['id']}")
        print(f"[LOG] NPCs en room: {[npc['id'] for npc in self.game.room_manager.load_npcs_in_room(self.game.players[player_id]['room'])]}")
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
        attacker = self.game.players.get(attacker_id, None)
        # print (f"[LOG-debug] Process turn for attacker ID: {attacker_id}, Victim ID: {victim_id}")
        # Determinar si la víctima es un NPC (_npc0,_npc1,..) o un jugador (0,1,2,..)
        if str(victim_id).startswith("_npc"):
            victim_is_npc = True
            victim = next(
                (npc for npc in self.game.room_manager.load_npcs_in_room(attacker["room"]) if npc["id"] == victim_id),
                None
            )
            if not victim:
                # Si el NPC ya no está en la sala, termina el combate
                self.game.mud.send_message(attacker_id, f"El combate con el NPC ha terminado porque ya no está en la sala.")
                del self.active_combats[attacker_id]
                return
        else:
            victim_is_npc = False
            victim = self.game.players.get(victim_id, None)
            if not victim:
                # Si el jugador ya no está disponible, termina el combate
                self.game.mud.send_message(attacker_id, f"El combate con el jugador ha terminado porque ya no está disponible.")
                del self.active_combats[attacker_id]
                return

        # Verificar si están en la misma sala
        if attacker["room"] != victim["room"]:
            self.game.mud.send_message(attacker_id, f"El combate con {victim['display_name']} ha terminado porque ya no están en la misma sala.")
            if not victim_is_npc:
                self.game.mud.send_message(victim_id, f"El combate con {attacker['display_name']} ha terminado porque ya no están en la misma sala.")
            del self.active_combats[attacker_id]
            if not victim_is_npc:
                del self.active_combats[victim_id]
            return

        # Verificar si el atacante tiene suficiente energía (solo jugadores)
        if attacker["e"] <= 0:
            self.game.mud.send_message(attacker_id, "No tienes suficiente energía para atacar.")
            if not victim_is_npc:
                self.game.mud.send_message(victim_id, f"{attacker['display_name']} intenta atacarte, pero está demasiado agotado.")
            combat["turn"] = victim_id
            return

        # Realizar la tirada de agilidad para determinar si el ataque tiene éxito
        rolla = random.randint(0, 5)
        rollv = random.randint(0, 5)
        chance = attacker["d"] + rolla - victim["a"] - rollv

        # Mensajes de tiradas si están activados
        if attacker_id in self.game.players and self.game.players[attacker_id]["config"].get("tiradas", False):
            self.game.mud.send_message(attacker_id, f"[info] Tirada Dest vs Agil: {attacker['d']} (Dest.A) + {rolla} - {victim['a']} (Agil.V) + {rollv} = {chance}")
        if not victim_is_npc and victim["config"].get("tiradas", False):
            self.game.mud.send_message(victim_id, f"[info] Tirada Dest vs Agil: {attacker['d']} (Dest.A) + {rolla} - {victim['a']} (Agil.V) + {rollv} = {chance}")

        if chance < 0:
            # El ataque falla
            self.game.mud.send_message(attacker_id, f"Tu ataque contra {victim['display_name']} ha fallado.")
            if not victim_is_npc:
                self.game.mud.send_message(victim_id, f"Has esquivado el ataque de {attacker['display_name']}.")
        else:
            # El ataque tiene éxito, calcular daño
            roll = random.randint(0, 5)
            damage = max(0, attacker["f"] + roll - victim["r"])
            victim["pv"] -= damage
            # guardar pv del atacante
            if victim_is_npc:
                # guardar los datos del npc en la base de datos
                self.game.room_manager.save_npc(victim)
            #if not attacker_id.startswith("_npc"):
            attacker["e"] -= 1  # Reducir energía del atacante (~~solo jugadores~~ jugadores y npc)

            # Mensajes de daño
            self.game.mud.send_message(attacker_id, f"Has infligido {damage} de daño a {victim['display_name']}.")
            if not victim_is_npc:
                self.game.mud.send_message(victim_id, f"Has recibido {damage} de daño de {attacker['display_name']}. Puntos de vida restantes: {victim['pv']}")

            # Verificar si la víctima ha muerto
            if victim["pv"] <= 0:
                if victim_is_npc:
                    self.game.mud.send_message(attacker_id, f"¡Has derrotado a {victim['display_name']}!")
                    del self.active_combats[attacker_id]
                    # Mensaje de muerte del NPC
                    self.game.mud.send_message(attacker_id, victim['dead_message'].replace('\\n', '\n'))
                    if victim['dead_effect']:
                        self.effect_manager.apply_effect(attacker_id, victim['dead_effect'], victim.get('dead_effect_message'))
                    # Programar respawn del NPC
                    from .npc_manager import schedule_npc_respawn
                    schedule_npc_respawn(victim, self.game.room_manager, self.game.players, self.game.mud)
                else:
                    self.end_combat(attacker_id, victim_id)
                return

        # Cambiar el turno
        combat["turn"] = victim_id

        if victim_is_npc:
            # Si la víctima es un NPC, programa su turno para atacar al jugador
            combat["timer"] = Timer(2, lambda: self.npc_attack(victim_id, attacker_id))
        else:
            # Si la víctima es un jugador, programa el turno del jugador
            self.active_combats[victim_id]["timer"] = Timer(2, lambda: self.process_turn(victim_id))
            combat["timer"] = None






    def npc_attack(self, npc_id, player_id):
        # Cargar el NPC y el jugador
        npc = next(
            (npc for npc in self.game.room_manager.load_npcs_in_room(self.game.players[player_id]["room"]) if npc["id"] == npc_id),
            None
        )
        player = self.game.players.get(player_id, None)

        if not npc or not player:
            # Si el NPC o el jugador ya no están disponibles, termina el combate
            print(f"[LOG] NPC {npc_id} o jugador {player_id} no disponibles. Terminando combate.")
            # ***** self.mud.send_message(player_id, f"El combate con {npc_id} ha terminado. Has escapado como un cobarde!!")
            self.game.mud.send_message(player_id, f"El combate ha terminado. Has escapado como un cobarde!!")
            del self.active_combats[player_id]
            return

        # Realizar la tirada de agilidad para determinar si el ataque tiene éxito
        rolla = random.randint(0, 5)
        rollv = random.randint(0, 5)
        chance = npc["d"] + rolla - player["a"] - rollv

        # Mensajes de tiradas si están activados
        if player["config"].get("tiradas", False):
            self.game.mud.send_message(player_id, f"[info] Tirada Dest vs Agil: {npc['d']} (Dest.NPC) + {rolla} - {player['a']} (Agil.J) + {rollv} = {chance}")

        if chance < 0:
            # El ataque del NPC falla
            self.game.mud.send_message(player_id, f"¡Has esquivado el ataque de {npc['display_name']}!")
        else:
            # El ataque del NPC tiene éxito, calcular daño
            roll = random.randint(0, 5)
            damage = max(0, npc["f"] + roll - player["r"])
            player["pv"] -= damage

            # Mensajes de daño
            self.game.mud.send_message(player_id, f"Has recibido {damage} de daño de {npc['display_name']}. Puntos de vida restantes: {player['pv']}")

            # Verificar si el jugador ha muerto
            if player["pv"] <= 0:
                self.game.mud.send_message(player_id, f"¡Has sido derrotado por {npc['display_name']}!")
                self.end_combat_npc(npc['display_name'], player_id)
                return

        # Cambiar el turno de vuelta al jugador
        self.active_combats[player_id]["timer"] = Timer(2, lambda: self.process_turn(player_id))






# *** intentar fusionar esta funcion con end_combat
    def end_combat_npc(self, npc_display_name, loser_id):
        del self.active_combats[loser_id]
        
        self.game.mud.send_message(loser_id, f"\033[31m¡Has sido derrotado por {npc_display_name}!\033[0m")
        self.game.mud.send_message(loser_id, f"\033[93mDebido a tu pobre genética, las celulas de tu cuerpo se deshacen lentamente debido a la falta de irrigación mantenida por tu bomba de fluido sanguíneo.\nPor imperativa del ordenador, los restos de tu triste cuerpo son trasladados a la planta de regeneración para ser reciclados y finalmene formar una nueva vida.\nTu alma y tu psique es transferida a un nuevo cuerpo.\033[0m")

        for pid, pl in self.game.players.items():
            if pid != loser_id:
                self.game.mud.send_message(pid, f"[info] {self.game.players[loser_id]['name']} ha muerto.")

        self.game.players[loser_id]["room"] = "respawn"
        self.game.players[loser_id]["clon"] += 1
        self.game.players[loser_id]["display_name"] = f"{self.game.players[loser_id]['name'].capitalize()}-{self.game.players[loser_id]['sector']}-{self.game.players[loser_id]['clon']}"
        self.game.players[loser_id]["pv"] = 25
        # Si el jugador ha alcanzado el límite de clones, se le informa y se archiva su patrón genético
        if self.game.players[loser_id]["clon"] >= 6:
            print(f"[LOG] Jugador {self.game.players[loser_id]['display_name']} ha alcanzado el límite de clones. Almacenando...")
            self.game.mud.send_message(loser_id, f"\033[97;;1mAtención, Ciudadano.\n"
                        f"Con la terminación de su sexta y última réplica clónica\n"
                        f", el Ordenador, en su incansable búsqueda de la optimización y felicidad para el Complejo Alfa, se ha visto en la imperativa necesidad de evaluar la viabilidad de su patrón genético\n"
                        f".\n"
                        f"Los registros detallados de su desempeño indican una tasa de recurrencia de fallos operativos y de adaptación que excede los parámetros aceptables para un servicio leal y eficiente\n"
                        f". Esta persistencia de anomalías a lo largo de todas las activaciones de su línea sugiere una desviación inerradicable en su secuencia genética, posiblemente resultado de una interferencia externa o un lamentable error de calibración en la fase de gestación. El Ordenador, que no comete errores, concluye que cualquier defecto presente debe ser ajeno a su propia programación inicial\n"
                        f".\n"
                        f"Por el bienestar colectivo y la salvaguarda de los valiosos recursos del Complejo Alfa\n"
                        f", su código genético ha sido marcado como inservible para el futuro progreso de la especie. Por tanto, y con efecto inmediato, su patrón genético será archivado permanentemente para un análisis póstumo en el Servicio Central de Procesamiento (SCP)\n"
                        f".\n"
                        f"Agradecemos su (reiterada) contribución y sacrificios en el cumplimiento de sus misiones.\n"
                        f"El Ordenador es su amigo.\033[0m\n")
            self.game.players[loser_id]["room"] = "lab/archivo_genetico"
            self.game.players[loser_id]["pv"] = 0
        # guardar los datos del jugador en la base de datos
        #self.player_manager.save_player(self.players[loser_id])





    def end_combat(self, winner_id, loser_id):
        del self.active_combats[winner_id]
        del self.active_combats[loser_id]

        self.game.mud.send_message(winner_id, f"\033[93m¡Has derrotado a {self.game.players[loser_id]['display_name']}!\033[0m")
        self.game.mud.send_message(loser_id, f"\033[31m¡Has sido derrotado por {self.game.players[winner_id]['display_name']}!\033[0m")
        self.game.mud.send_message(loser_id, f"\033[93mDebido a tu pobre genética, las celulas de tu cuerpo se deshacen lentamente debido a la falta de irrigación mantenida por tu bomba de fluido sanguíneo.\nPor imperativa del ordenador, los restos de tu triste cuerpo son trasladados a la planta de regeneración para ser reciclados y finalmene formar una nueva vida.\nTu alma y tu psique es transferida a un nuevo cuerpo.\033[0m")

        for pid, pl in self.game.players.items():
            if pid != loser_id:
                self.game.mud.send_message(pid, f"[info] {self.game.players[loser_id]['name']} ha muerto.")

        self.game.players[loser_id]["room"] = "respawn"
        self.game.players[loser_id]["clon"] += 1
        self.game.players[loser_id]["display_name"] = f"{self.game.players[loser_id]['name'].capitalize()}-{self.game.players[loser_id]['sector']}-{self.game.players[loser_id]['clon']}"
        self.game.players[loser_id]["pv"] = 25
        # Si el jugador ha alcanzado el límite de clones, se le informa y se archiva su patrón genético
        if self.game.players[loser_id]["clon"] >= 6:
            print(f"[LOG] Jugador {self.game.players[loser_id]['display_name']} ha alcanzado el límite de clones. Almacenando...")
            self.game.mud.send_message(loser_id, f"\033[97;;1mAtención, Ciudadano.\n"
                        f"Con la terminación de su sexta y última réplica clónica\n"
                        f", el Ordenador, en su incansable búsqueda de la optimización y felicidad para el Complejo Alfa, se ha visto en la imperativa necesidad de evaluar la viabilidad de su patrón genético\n"
                        f".\n"
                        f"Los registros detallados de su desempeño indican una tasa de recurrencia de fallos operativos y de adaptación que excede los parámetros aceptables para un servicio leal y eficiente\n"
                        f". Esta persistencia de anomalías a lo largo de todas las activaciones de su línea sugiere una desviación inerradicable en su secuencia genética, posiblemente resultado de una interferencia externa o un lamentable error de calibración en la fase de gestación. El Ordenador, que no comete errores, concluye que cualquier defecto presente debe ser ajeno a su propia programación inicial\n"
                        f".\n"
                        f"Por el bienestar colectivo y la salvaguarda de los valiosos recursos del Complejo Alfa\n"
                        f", su código genético ha sido marcado como inservible para el futuro progreso de la especie. Por tanto, y con efecto inmediato, su patrón genético será archivado permanentemente para un análisis póstumo en el Servicio Central de Procesamiento (SCP)\n"
                        f".\n"
                        f"Agradecemos su (reiterada) contribución y sacrificios en el cumplimiento de sus misiones.\n"
                        f"El Ordenador es su amigo.\033[0m\n")
            self.game.players[loser_id]["room"] = "lab/archivo_genetico"
            self.game.players[loser_id]["pv"] = 0
        # guardar los datos del jugador en la base de datos
        #self.player_manager.save_player(self.players[loser_id])
