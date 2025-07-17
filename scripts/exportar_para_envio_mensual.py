import csv
import psycopg2
import os
from datetime import date
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

def exportar_correo_mensual(fecha_ref=None):
    fecha_ref = fecha_ref or date.today()
    anio_actual = fecha_ref.year
    mes_actual = fecha_ref.month

    query = """
        SELECT e.correo, %s AS fecha, FALSE AS baja
        FROM empresas e
        WHERE NOT EXISTS (
            SELECT 1 FROM envios_mail em
            WHERE em.id_empresa = e.id
              AND EXTRACT(YEAR FROM em.fecha_envio) = %s
              AND EXTRACT(MONTH FROM em.fecha_envio) = %s
        )
    """

    export_file = EXPORT_PATH / f"correos_pendientes_mes_{fecha_ref.strftime('%Y_%m')}.csv"

    with psycopg2.connect(**DB_CONFIG) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (fecha_ref, anio_actual, mes_actual))
        rows = cursor.fetchall()

        with open(export_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(['correo', 'fecha', 'baja'])
            writer.writerows(rows)

    print(f"Exportación completada: {export_file} ({len(rows)} correos este mes)")

if __name__ == "__main__":
    exportar_correo_mensual()
