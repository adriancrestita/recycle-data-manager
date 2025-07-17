import csv
import psycopg2
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

EXPORT_PATH = Path(__file__).parent.parent / "exports"
EXPORT_PATH.mkdir(exist_ok=True)

def exportar_historial():
    query = """
        SELECT e.nombre, e.correo, em.fecha_envio, em.estado, em.error
        FROM empresas e
        JOIN envios_mail em ON em.id_empresa = e.id
        ORDER BY e.nombre, em.fecha_envio;
    """

    export_file = EXPORT_PATH / "historial_mailings.csv"

    with psycopg2.connect(**DB_CONFIG) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        with open(export_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(['nombre', 'correo', 'fecha_envio', 'estado', 'error'])
            writer.writerows(rows)

    print(f"Historial exportado a: {export_file} ({len(rows)} registros)")

if __name__ == "__main__":
    exportar_historial()
