import sqlite3
import random
import json
from .config import NIVEL_DISPLAY, NIVEL_COLOR

class PlayerManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def create_player(self, name, password):
        puntos = 0
        while puntos < 80: # Asegurarse de que la suma de atributos sea al menos 80
            f = random.randint(1, 20)
            r = random.randint(1, 20)
            a = random.randint(1, 20)
            d = random.randint(1, 20)
            p = random.randint(1, 20)
            c = random.randint(1, 20)
            tm = random.randint(1, 20)
            pm = random.randint(1, 20)
            puntos = f + r + a + d + p + c + tm + pm
        ficha = {
            "name": name,"password": password,"nivel": 0,"clon": 1,"pv": 100,"e": 100,"f": f,"r": r,"a": a,"d": d,"p": p,"c": c,"tm": tm,"pm": pm,"servicio": None,"sociedad_secreta": None,"sector": None,"room": "inicio","config": {},"inventario": {},"traicion": 0
        }
        # Servicio
        servicio_roll = random.randint(1, 20)
        if servicio_roll <= 2:
            ficha["servicio"] = "SSI"
        elif servicio_roll <= 4:
            ficha["servicio"] = "STC"
        elif servicio_roll <= 8:
            ficha["servicio"] = "SBD"
        elif servicio_roll <= 11:
            ficha["servicio"] = "SDF"
        elif servicio_roll <= 14:
            ficha["servicio"] = "SPL"
        elif servicio_roll <= 16:
            ficha["servicio"] = "SEG"
        elif servicio_roll <= 18:
            ficha["servicio"] = "SID"
        else:
            ficha["servicio"] = "SCP"
        # Sociedad secreta
        sociedad_roll = random.randint(1, 8)
        if sociedad_roll <= 2:
            ficha["sociedad_secreta"] = "Antimutantes"
        elif sociedad_roll <= 4:
            ficha["sociedad_secreta"] = "Piratas Informáticos"
        elif sociedad_roll <= 6:
            ficha["sociedad_secreta"] = "Comunistas"
        else:
            ficha["sociedad_secreta"] = "Iglesia Primitiva del Cristo Programador"
        # Sector
        sector_roll = random.randint(1, 8)
        if sector_roll <= 2:
            ficha["sector"] = "OTE"
        elif sector_roll <= 4:
            ficha["sector"] = "EKO"
        elif sector_roll <= 6:
            ficha["sector"] = "ANO"
        else:
            ficha["sector"] = "ICO"

        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO players (name, password, nivel, clon, pv, e, f, r, a, d, p, c, tm, pm, servicio, sociedad_secreta, sector, room, config, inventario, traicion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ficha["name"], ficha["password"], ficha["nivel"], ficha["clon"], ficha["pv"], ficha["e"], ficha["f"], ficha["r"], ficha["a"],
            ficha["d"], ficha["p"], ficha["c"], ficha["tm"], ficha["pm"], ficha["servicio"],
            ficha["sociedad_secreta"], ficha["sector"], ficha["room"],
            json.dumps(ficha.get("config", {})), json.dumps(ficha.get("inventario", {})), ficha.get("traicion", 0)
        ))
        conn.commit()
        conn.close()

        ficha["display_name"] = f"{ficha['name'].capitalize()}-{ficha['sector']}-{ficha['clon']}"
        print(f"[LOG] Jugador creado: {ficha['display_name']}")
        return ficha

    def load_player(self, name):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM players WHERE name = ?", (name.lower(),))
        row = cur.fetchone()
        conn.close()
        if not row:
            # raise ValueError("Jugador no encontrado.")
            print(f"[WRN] Error loading player (name= {name}): Jugador no encontrado. Crear?")
            return None
        ficha = dict(row)
        ficha["config"] = json.loads(ficha.get("config", "{}") or "{}")  # Manejar None o vacío
        ficha["inventario"] = json.loads(ficha.get("inventario", "{}") or "{}")  # Manejar None o vacío
        if ficha.get("nivel") > 0:
            ficha["display_name"] = f"{NIVEL_COLOR.get(ficha.get('nivel', 0))}{ficha['name'].capitalize()}-{NIVEL_DISPLAY.get(ficha.get('nivel', 0))}-{ficha['sector']}-{ficha['clon']}{NIVEL_COLOR.get('reset')}"
        else:
            ficha["display_name"] = f"{ficha['name'].capitalize()}-{ficha['sector']}-{ficha['clon']}"
        
        return ficha

    def save_player(self, ficha):
        if ficha.get("clon"): # existe el jugador
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute("""
                UPDATE players SET
                    nivel = ?, clon = ?, pv = ?, e = ?, f = ?, r = ?, a = ?, d = ?, p = ?, c = ?, tm = ?, pm = ?,
                    servicio = ?, sociedad_secreta = ?, sector = ?, room = ?, config = ?, inventario = ?, traicion = ?
                WHERE name = ?
            """, (
                ficha.get("nivel", 0), ficha.get("clon", 1), ficha["pv"], ficha["e"], ficha["f"], ficha["r"], ficha["a"], ficha["d"],
                ficha["p"], ficha["c"], ficha["tm"], ficha["pm"], ficha["servicio"], ficha["sociedad_secreta"], ficha.get("sector", None), ficha["room"],
                json.dumps(ficha.get("config", {})), json.dumps(ficha.get("inventario", {})), ficha.get("traicion", 0), ficha["name"]
            ))
            conn.commit()
            conn.close()
            print(f"[LOG] Jugador guardado: {ficha['display_name']}")
        else: # no existe el jugador
            print(f"[WRN] Error saving player (name= {ficha['name']}): Jugador no encontrado. Crear?")


    def validate_password(self, name, password):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT password FROM players WHERE name = ?", (name.lower(),))
        row = cur.fetchone()
        conn.close()
        if row and row["password"] == password:
            return True
        elif row:
            raise ValueError("Contraseña incorrecta.")
        return False
