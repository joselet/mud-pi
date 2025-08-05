import os
import sqlite3

def execute_sql_file(db_path, sql_file_path):
    """Ejecuta un fichero SQL en la base de datos especificada."""
    try:
        with open(sql_file_path, 'r', encoding='utf-8') as sql_file:
            sql_script = sql_file.read()
        with sqlite3.connect(db_path) as conn:
            conn.executescript(sql_script)
        print(f"Ejecutado correctamente: {sql_file_path}")
    except Exception as e:
        print(f"Error al ejecutar {sql_file_path}: {e}")

def initialize_database():
    """Crea la base de datos y ejecuta los scripts SQL necesarios."""
    db_path = os.path.join("..", "data", "mud.db")
    sql_files = [
        "insert_rooms.sql",
        "insert_objects_npcs.sql",
        "schema_players.sql"
    ]
    
    # Crear el directorio ../data si no existe
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Crear la base de datos si no existe
    if not os.path.exists(db_path):
        print(f"Creando la base de datos en {db_path}...")
        open(db_path, 'w').close()  # Crear un archivo vacío
    else:
        print(f"La base de datos ya existe en {db_path}. Sobrescribiendo datos...")

    # Ejecutar cada fichero SQL
    for sql_file in sql_files:
        if os.path.exists(sql_file):
            execute_sql_file(db_path, sql_file)
        else:
            print(f"Fichero SQL no encontrado: {sql_file}")

if __name__ == "__main__":
    initialize_database()