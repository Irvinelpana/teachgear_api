from flask import Blueprint, jsonify, request
import pymysql.cursors
from db import get_db_connection

clientes_bp = Blueprint('clientes_api', __name__, url_prefix='/api/v1/clientes')

# 1. GET - Obtener todos los clientes
@clientes_bp.route('', methods=['GET'])
def get_clientes():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM cliente")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(clientes)

# 2. POST - Crear cliente
@clientes_bp.route('', methods=['POST'])
def create_cliente():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "INSERT INTO cliente (nombre, apellido, email, telefono) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (data['nombre'], data['apellido'], data['email'], data.get('telefono')))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "Cliente registrado correctamente"}), 201

# 3. GET - Obtener cliente por ID
@clientes_bp.route('/<int:id>', methods=['GET'])
def get_cliente_id(id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM cliente WHERE cliente_id = %s", (id,))
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404
    return jsonify(cliente)

# 4. PUT - Actualizar cliente por ID
@clientes_bp.route('/<int:id>', methods=['PUT'])
def update_cliente(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "UPDATE cliente SET nombre=%s, apellido=%s, email=%s, telefono=%s WHERE cliente_id=%s"
    cursor.execute(sql, (data['nombre'], data['apellido'], data['email'], data.get('telefono'), id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": f"Cliente con ID {id} actualizado correctamente"})

# 5. DELETE - Eliminar cliente por ID
@clientes_bp.route('/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("DELETE FROM cliente WHERE cliente_id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": f"Cliente con ID {id} eliminado correctamente"})

# --- ENDPOINT RELACIÓN 1:N (Dirección asociada a cliente_id) ---
@clientes_bp.route('/direcciones', methods=['POST'])
def create_direccion():
    data = request.json
    cliente_id = data.get('cliente_id')

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Validar que exista el cliente_id antes de insertar la direccion
    cursor.execute("SELECT cliente_id FROM cliente WHERE cliente_id = %s", (cliente_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"error": f"El cliente con ID {cliente_id} no existe."}), 400

    sql = "INSERT INTO direccion (cliente_id, calle_numero, colonia, ciudad, codigo_postal) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (cliente_id, data['calle_numero'], data['colonia'], data['ciudad'], data['codigo_postal']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "Dirección registrada al cliente correctamente"}), 201