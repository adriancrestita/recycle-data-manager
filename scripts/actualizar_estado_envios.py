import psycopg2
from dotenv import load_dotenv
import os

# Cargar el archivo .env desde la carpeta config
load_dotenv(dotenv_path="./config/.env")

def actualizar_envios_pendientes():
    try:
        conn = psycopg2.connect(os.getenv("DB_URL"))
        cur = conn.cursor()

        query = """
        UPDATE envios_mail
        SET estado = 'pendiente'
        WHERE estado = 'enviado'
          AND fecha_envio < date_trunc('month', CURRENT_DATE);
        """

        cur.execute(query)
        actualizados = cur.rowcount

        conn.commit()
        cur.close()
        conn.close()

        print(f"[✓] Registros actualizados a 'pendiente': {actualizados}")

    except Exception as e:
        print(f"[✗] Error al actualizar registros: {e}")

if __name__ == "__main__":
    actualizar_envios_pendientes()
