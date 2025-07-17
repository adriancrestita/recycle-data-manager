import csv
import psycopg2
import re
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

CSV_PATH = Path(__file__).parent.parent / "db" / "seed" / "empresas.csv"
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

def email_valido(email):
    return re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email)

def cargar_empresas():
    registros_insertados = 0
    errores = []

    with psycopg2.connect(**DB_CONFIG) as conn:
        cursor = conn.cursor()
        with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for i, row in enumerate(reader, start=1):
                correo = row['correo'].strip()
                if not email_valido(correo):
                    errores.append(f"Fila {i}: Email inválido ({correo})")
                    continue

                cursor.execute("SELECT 1 FROM empresas WHERE correo = %s", (correo,))
                if cursor.fetchone():
                    errores.append(f"Fila {i}: Correo duplicado ({correo})")
                    continue

                cursor.execute("""
                    INSERT INTO empresas (nombre, correo, telefono, provincia, direccion, cp, url_web, sector)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    row['nombre'], correo, row['telefono'], row['provincia'],
                    row['direccion'], row['cp'], row['url_web'], row['sector']
                ))
                registros_insertados += 1

        conn.commit()

    log_path = LOG_DIR / f"import_empresas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    with open(log_path, "w", encoding="utf-8") as log_file:
        for err in errores:
            log_file.write(f"ERROR: {err}\n")
        log_file.write(f"\nTotal insertados: {registros_insertados}\n")

    print(f"Importación finalizada. Insertados: {registros_insertados}. Errores: {len(errores)}")
    print(f"Log: {log_path}")

if __name__ == "__main__":
    cargar_empresas()
