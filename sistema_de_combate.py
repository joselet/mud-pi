import random

combates_activos = {}

def iniciar_combate(players, atacante_id, victima_nombre, mud):
    # Procesar el nombre de la víctima para garantizar consistencia
    victima_nombre = victima_nombre.strip().lower()

    # Buscar el ID de la víctima de manera consistente
    victima_id = None
    for pid, pl in players.items():
        if pl["name"].strip().lower() == victima_nombre:
            victima_id = pid
            break

    # Verificar si no se encontró un ID válido
    if victima_id is None:
        mud.send_message(atacante_id, f"No se encontró al jugador '{victima_nombre}'.")
        return

    # Registrar el combate si no está ya activo
    if atacante_id in combates_activos or victima_id in combates_activos:
        mud.send_message(atacante_id, "Ya estás en un combate.")
        return

    combates_activos[atacante_id] = {"victima": victima_id, "turno": atacante_id}
    combates_activos[victima_id] = {"victima": atacante_id, "turno": atacante_id}

    # Notificar a los jugadores
    mud.send_message(atacante_id, f"Has iniciado un combate contra {players[victima_id]['name']}.")
    mud.send_message(victima_id, f"{players[atacante_id]['name']} te ha atacado. ¡Prepárate para luchar!")

def procesar_turno_combate(players, mud, mostrar_sala_al_jugador):
    for atacante_id, combate in list(combates_activos.items()):
        # Solo procesar el turno del atacante actual
        if combate["turno"] != atacante_id:
            continue

        victima_id = combate["victima"]
        atacante = players[atacante_id]
        victima = players[victima_id]

        # Verificar si el atacante tiene suficiente energía
        if atacante["e"] <= 0:
            mud.send_message(atacante_id, "No tienes suficiente energía para atacar.")
            combate["turno"] = victima_id  # Pasar el turno a la víctima
            continue

        # Calcular daño
        tirada = random.randint(0, 5)
        dano = max(0, atacante["f"] + tirada - victima["d"])
        victima["pv"] -= dano
        atacante["e"] -= 1  # Restar energía al atacante

        # Notificar a los jugadores
        mud.send_message(atacante_id, f"Tirada: {atacante['f']} (Fue.A) + {tirada} - {victima['d']} (Des.D) = {dano}\nHas infligido {dano} de daño a {victima['display_name']}.")
        mud.send_message(victima_id, f"Tirada: {atacante['f']} (Fue.A) + {tirada} - {victima['d']} (Des.D) = {dano}\nHas recibido {dano} de daño de {atacante['display_name']}.\nPuntos de vida restantes: {victima['pv']}")

        # Verificar si la víctima ha muerto
        if victima["pv"] <= 0:
            mud.send_message(atacante_id, f"\033[93m¡Has derrotado a {victima['display_name']}!\033[0m")
            mud.send_message(victima_id, "\033[31m¡Has sido derrotado!\033[0m")
            mud.send_message(victima_id, "\033[93mDebido a tu pobre genética, las celulas de tu cuerpo se deshacen lentamente debido a la falta de irrigación mantenida por tu bomba de fluido sanguíneo.\nPor imperativa del ordenador, los restos de tu triste cuerpo son trasladados a la planta de regeneración para ser reciclados y finalmene formar una nueva vida.\nTu alma y tu psique es transferida a un nuevo cuerpo.\033[0m")
            finalizar_combate(atacante_id, victima_id, players, mud, mostrar_sala_al_jugador)
            continue

        # Pasar el turno a la víctima
        combate["turno"] = victima_id

        # Respuesta automática de la víctima
        if victima["e"] > 0:
            respuesta_tirada = random.randint(0, 5)
            respuesta_dano = max(0, victima["f"] + respuesta_tirada - atacante["d"])
            atacante["pv"] -= respuesta_dano
            victima["e"] -= 1  # Restar energía a la víctima

            # Notificar a los jugadores
            mud.send_message(victima_id, f"En respuesta, Has infligido {respuesta_dano} de daño a {atacante['display_name']}.\nTirada: {victima['f']} (Fue.V) + {respuesta_tirada} - {atacante['d']} (Des.A) = {respuesta_dano}")
            mud.send_message(atacante_id, f"En respuesta, Has recibido {respuesta_dano} de daño de {victima['display_name']}.\nTirada: {victima['f']} (Fue.V) + {respuesta_tirada} - {atacante['d']} (Des.A) = {respuesta_dano}\nPuntos de vida restantes: {atacante['pv']}")

            # Verificar si el atacante ha muerto
            if atacante["pv"] <= 0:
                mud.send_message(victima_id, f"\033[93m¡Has derrotado a {atacante['display_name']}!\033[0m")
                mud.send_message(atacante_id, "\033[31m¡Has sido derrotado!\033[0m")
                finalizar_combate(victima_id, atacante_id, players, mud, mostrar_sala_al_jugador)

def finalizar_combate(ganador_id, perdedor_id, players, mud, mostrar_sala_al_jugador):
    """Finaliza el combate entre dos jugadores."""
    del combates_activos[ganador_id]
    del combates_activos[perdedor_id]

    # Enviar al perdedor a la sala de incubadora
    players[perdedor_id]["room"] = "respawn"
    mostrar_sala_al_jugador(perdedor_id)

    # Incrementar el clon del perdedor
    players[perdedor_id]["clon"] += 1
    players[perdedor_id]["display_name"] = f"{players[perdedor_id]['name'].capitalize()}-{players[perdedor_id]['sector']}-{players[perdedor_id]['clon']}"

    # Restablecer un porcentaje de la vida del perdedor
    players[perdedor_id]["pv"] = 25

    # Notificar a todos los jugadores que alguien ha muerto
    for pid, pl in players.items():
        if pid != perdedor_id:
            mud.send_message(pid, f"[info] {players[perdedor_id]['name']} ha muerto.")
