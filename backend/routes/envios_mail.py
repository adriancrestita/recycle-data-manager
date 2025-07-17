from flask import Blueprint, request, jsonify
from backend.models.db import get_db_connection
from datetime import datetime

bp = Blueprint('envios_mail', __name__)

@bp.route('/api/envios_mail/log', methods=['POST'])
def registrar_envio():
    data = request.get_json()

    correo = data.get('correo')
    fecha_envio = data.get('fecha_envio')
    estado = data.get('estado', 'pendiente')
    error = data.get('error', '')

    if not correo or not fecha_envio:
        return jsonify({"error": "Faltan campos obligatorios (correo, fecha_envio)"}), 400

    try:
        fecha_envio = datetime.strptime(fecha_envio, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}), 400

    if estado not in ('enviado', 'pendiente', 'error'):
        return jsonify({"error": "Estado inválido"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM empresas WHERE correo = %s", (correo,))
    empresa = cur.fetchone()

    if not empresa:
        return jsonify({"error": f"Empresa no encontrada para el correo: {correo}"}), 404

    id_empresa = empresa[0]

    cur.execute("""
        SELECT id FROM envios_mail
        WHERE id_empresa = %s AND fecha_envio = %s
    """, (id_empresa, fecha_envio))
    envio = cur.fetchone()

    if envio:
        cur.execute("""
            UPDATE envios_mail
            SET estado = %s, error = %s
            WHERE id = %s
        """, (estado, error, envio[0]))
    else:
        cur.execute("""
            INSERT INTO envios_mail (id_empresa, fecha_envio, estado, baja, error)
            VALUES (%s, %s, %s, FALSE, %s)
        """, (id_empresa, fecha_envio, estado, error))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": f"Registro actualizado para {correo} - {estado}"}), 200
