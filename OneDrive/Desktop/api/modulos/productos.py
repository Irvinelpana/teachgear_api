from flask import Blueprint, jsonify, request
import pymysql.cursors
from db import get_db_connection

productos_bp = Blueprint('productos_api', __name__, url_prefix='/api/v1/producto')

# 1. GET - Obtener todos los productos
@productos_bp.route('', methods=['GET'])
def get_productos():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM producto")
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(productos)

# 2. POST - Crear producto
@productos_bp.route('', methods=['POST'])
def create_producto():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "INSERT INTO producto (nombre, categoria, precio, stock, descripcion) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (data['nombre'], data['categoria'], data['precio'], data['stock'], data.get('descripcion', '')))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "Producto guardado con éxito"}), 201

# 3. GET - Obtener un producto por ID
@productos_bp.route('/<int:id>', methods=['GET'])
def get_producto_id(id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM producto WHERE producto_id = %s", (id,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify(producto)

# 4. PUT - Actualizar producto por ID
@productos_bp.route('/<int:id>', methods=['PUT'])
def update_producto(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "UPDATE producto SET nombre=%s, categoria=%s, precio=%s, stock=%s, descripcion=%s WHERE producto_id=%s"
    cursor.execute(sql, (data['nombre'], data['categoria'], data['precio'], data['stock'], data.get('descripcion', ''), id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": f"Producto con ID {id} actualizado correctamente"})

# 5. DELETE - Eliminar producto por ID
@productos_bp.route('/<int:id>', methods=['DELETE'])
def delete_producto(id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("DELETE FROM producto WHERE producto_id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": f"Producto con ID {id} eliminado correctamente"})