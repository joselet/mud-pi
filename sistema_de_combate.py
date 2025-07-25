import random

combates_activos = {}

def iniciar_combate(players, atacante_id, victima_nombre, mud):
    # Procesar el nombre de la víctima para garantizar consistencia
    victima_nombre = victima_nombre.strip().lower()

    # Buscar el ID de la víctima de manera consistente
    victima_id = None
    for pid, pl in players.items():
        processed_name = pl["name"].strip().lower()
        #mud.send_message(atacante_id, f"Debug: Comparando '{victima_nombre}' con '{processed_name}' (ID: {pid})")
        if processed_name == victima_nombre:
            victima_id = pid
            #mud.send_message(atacante_id, f"Debug: Encontrado ID de víctima: {victima_id}")
            break

    # Verificar si no se encontró un ID válido
    if victima_id is None:  # Cambiado de `if not victima_id:` a `if victima_id is None:`
        mud.send_message(atacante_id, f"No se encontró al jugador '{victima_nombre}' (sin victima_id).")
        return

    # Registrar el combate
    combates_activos[atacante_id] = {"victima": victima_id, "turno": atacante_id}
    combates_activos[victima_id] = {"victima": atacante_id, "turno": atacante_id}

    # Notificar a los jugadores
    mud.send_message(atacante_id, f"Has iniciado un combate contra {players[victima_id]['name']}.")
    mud.send_message(victima_id, f"{players[atacante_id]['name']} te ha atacado. ¡Prepárate para luchar!")

def procesar_turno_combate(players, mud, mostrar_sala_al_jugador):
    for atacante_id, combate in list(combates_activos.items()):
        if combate["turno"] != atacante_id:
            continue

        victima_id = combate["victima"]
        atacante = players[atacante_id]
        victima = players[victima_id]
        # Verificar si el atacante tiene suficiente energía
        if atacante["e"] <= 0:
            mud.send_message(atacante_id, "No tienes suficiente energía para atacar.")
            continue
        # Calcular daño
        tirada = random.randint(0, 5)
        dano = max(0, atacante["f"] + tirada - victima["d"])
        victima["pv"] -= dano
        # Restar energía al atacante
        atacante["e"] -= 1
        # Notificar a los jugadores
        mud.send_message(atacante_id, f"Has infligido {dano} de daño a {players[victima_id]['display_name']}.\nTirada:  {atacante['f']}(Fue.A) + {tirada} - {victima['d']}(Des.D)")
        mud.send_message(victima_id, f"Has recibido {dano} de daño de {players[atacante_id]['display_name']}.\nTirada:  {atacante['f']}(Fue.A) + {tirada} - {victima['d']}(Des.D)\nPuntos de vida restantes: {victima['pv']}")

        # Verificar si la víctima ha muerto
        if victima["pv"] <= 0:
            mud.send_message(atacante_id, f"\033[93m¡Has derrotado a {players[victima_id]['name']}!\033[0m")
            mud.send_message(victima_id, "\033[31m¡Has sido derrotado!\033[0m")
            mud.send_message(victima_id, "\033[93mDebido a tu pobre genética, las celulas de tu cuerpo se deshacen lentamente debido a la falta de irrigación mantenida por tu bomba de fluido sanguíneo.\nPor imperativa del ordenador, los restos de tu triste cuerpo son trasladados a la planta de regeneración para ser reciclados y finalmene formar una nueva vida.\nTu alma y tu psique es transferida a un nuevo cuerpo.\033[0m")
            del combates_activos[atacante_id]
            del combates_activos[victima_id]
            # enviar a la víctima a la sala de incubadora
            players[victima_id]["room"] = "respawn"
            mostrar_sala_al_jugador(victima_id)
            # aumenter el clon del jugador
            players[victima_id]["clon"] += 1
            # actualizar display_namef"{ficha['name'].capitalize()}-{ficha['sector']}-{ficha['clon']}"
            players[victima_id]["display_name"] = f"{players[victima_id]['name'].capitalize()}-{players[victima_id]['sector']}-{players[victima_id]['clon']}"
            # restablecer un porcentaje de la vida de la víctima
            victima["pv"] = 25
            # Notificar a todos los jugadores que alguien ha muerto
            for pid, pl in players.items():
                if pid != victima_id:
                    mud.send_message(pid, f"[info] {players[victima_id]['name']} Ha muerto.")
            # Terminar el combate
            continue
        else:
            combate["turno"] = victima_id
