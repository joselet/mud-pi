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

def procesar_turno_combate(players, mud,mostrar_sala_al_jugador):
    for atacante_id, combate in list(combates_activos.items()):
        if combate["turno"] != atacante_id:
            continue

        victima_id = combate["victima"]
        atacante = players[atacante_id]["ficha"]
        victima = players[victima_id]["ficha"]
        # Verificar si el atacante tiene suficiente energía
        if atacante["energia"] <= 0:
            mud.send_message(atacante_id, "No tienes suficiente energía para atacar.")
            continue
        # Calcular daño
        dano = max(0, atacante["fuerza"] + random.randint(0, 5) - victima["destreza"])
        victima["vida"] -= dano
        # Restar energía al atacante
        atacante["energia"] -= 1
        # Notificar a los jugadores
        mud.send_message(atacante_id, f"Has infligido {dano} de daño a {players[victima_id]['name']}.")
        mud.send_message(victima_id, f"Has recibido {dano} de daño de {players[atacante_id]['name']}.")

        # Verificar si la víctima ha muerto
        if victima["vida"] <= 0:
            mud.send_message(atacante_id, f"¡Has derrotado a {players[victima_id]['name']}!")
            mud.send_message(victima_id, "¡Has sido derrotado!")
            del combates_activos[atacante_id]
            del combates_activos[victima_id]
            # enviar a la víctima a la sala de incubadora
            players[victima_id]["room"] = "incubadora"
            mostrar_sala_al_jugador(victima_id, mud)
            # restablecer la vida de la víctima
            victima["vida"] = 100
            # Notificar a todos los jugadores que alguien ha muerto
            for pid, pl in players.items():
                if pid != victima_id:
                    mud.send_message(pid, f"[info] {players[id]['name']} Ha muerto.")
            # Terminar el combate
            continue
        else:
            combate["turno"] = victima_id
