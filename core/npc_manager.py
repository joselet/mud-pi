import threading

def schedule_npc_respawn(npc, room_manager, players, mud):
    """
    Programa el respawn de un NPC después de su tiempo de respawn.
    """
    def respawn():
        npc["pv"] = npc["pv_max"]
        room_manager.save_npc(npc)
        print(f"[LOG] NPC {npc['display_name']} ha respawneado en la sala {npc['room']}.")

        # Notificar a los jugadores en la sala del respawn del NPC
        for player_id in room_manager.players_in_room(npc["room"], players):
            mud.send_message(player_id, f"{npc['display_name']} irrumpe aquí de repente.")

    respawn_time = npc.get("respawn_time", 3600)  # Tiempo de respawn en segundos (default: 3600)
    threading.Timer(respawn_time, respawn).start()

