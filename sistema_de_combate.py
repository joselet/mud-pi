import random

combates_activos = {}

def iniciar_combate(players, atacante_id, victima_nombre, mud):
    victima_id = next((pid for pid, pl in players.items() if pl["name"] == victima_nombre), None)
    if not victima_id:
        mud.send_message(atacante_id, f"No se encontró al jugador '{victima_nombre}'.")
        return

    combates_activos[atacante_id] = {"victima": victima_id, "turno": atacante_id}
    combates_activos[victima_id] = {"victima": atacante_id, "turno": atacante_id}

    mud.send_message(atacante_id, f"Has iniciado un combate contra {victima_nombre}.")
    mud.send_message(victima_id, f"{players[atacante_id]['name']} te ha atacado. ¡Prepárate para luchar!")

def procesar_turno_combate(players, mud):
    for atacante_id, combate in list(combates_activos.items()):
        if combate["turno"] != atacante_id:
            continue

        victima_id = combate["victima"]
        atacante = players[atacante_id]["ficha"]
        victima = players[victima_id]["ficha"]

        # Calcular daño
        dano = max(0, atacante["fuerza"] + random.randint(-5, 5) - victima["destreza"])
        victima["vida"] -= dano

        mud.send_message(atacante_id, f"Has infligido {dano} de daño a {players[victima_id]['name']}.")
        mud.send_message(victima_id, f"Has recibido {dano} de daño de {players[atacante_id]['name']}.")

        # Verificar si la víctima ha muerto
        if victima["vida"] <= 0:
            mud.send_message(atacante_id, f"¡Has derrotado a {players[victima_id]['name']}!")
            mud.send_message(victima_id, "¡Has sido derrotado!")
            del combates_activos[atacante_id]
            del combates_activos[victima_id]
        else:
            combate["turno"] = victima_id
