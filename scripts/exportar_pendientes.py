import csv
import os
import psycopg2
from dotenv import load_dotenv

# Cargar configuración
load_dotenv(dotenv_path="./config/.env")

EXPORT_DIR = "./exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

def exportar_correos_pendientes(nombre_archivo_csv="pendientes_envio.csv"):
    try:
        conn = psycopg2.connect(os.getenv("DB_URL"))
        cur = conn.cursor()

        query = """
        SELECT e.correo, em.fecha_envio, em.baja
        FROM envios_mail em
        JOIN empresas e ON em.id_empresa = e.id
        WHERE em.estado = 'pendiente' AND em.baja = FALSE;
        """

        cur.execute(query)
        registros = cur.fetchall()

        ruta_csv = os.path.join(EXPORT_DIR, nombre_archivo_csv)

        with open(ruta_csv, mode='w', newline='') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(["correo", "fecha_envio", "baja"])  # encabezado
            writer.writerows(registros)

        print(f"[✓] Exportación completada: {ruta_csv} ({len(registros)} registros)")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"[✗] Error al exportar correos pendientes: {e}")

if __name__ == "__main__":
    exportar_correos_pendientes()
