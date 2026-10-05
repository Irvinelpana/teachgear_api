from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'perez',
    'password': 'perez123',
    'database': 'techgear_db'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# 1. GET ALL
@app.route('/api/v1/producto', methods=['GET'])
def get_productos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM producto")
        productos = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(productos), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 2. GET BY ID
@app.route('/api/v1/producto/<int:id>', methods=['GET'])
def get_producto(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM producto WHERE producto_id = %s", (id,))
        producto = cursor.fetchone()
        cursor.close()
        conn.close()

        if producto:
            return jsonify(producto), 200
        else:
            return jsonify({"status": "error", "message": "Producto no encontrado"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 3. POST
@app.route('/api/v1/producto', methods=['POST'])
def create_producto():
    data = request.get_json()
    if not data or not all(k in data for k in ('nombre', 'precio', 'stock', 'categoria')):
        return jsonify({"status": "error", "message": "Faltan campos obligatorios"}), 400

    descripcion = data.get('descripcion', None)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO producto (nombre, categoria, precio, stock, descripcion) VALUES (%s, %s, %s, %s, %s)"
        values = (data['nombre'], data['categoria'], data['precio'], data['stock'], descripcion)
        cursor.execute(query, values)
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "Registro creado exitosamente",
            "id": new_id
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 4. PUT
@app.route('/api/v1/producto/<int:id>', methods=['PUT'])
def update_producto(id):
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Datos de actualización vacíos"}), 400

    descripcion = data.get('descripcion', None)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT producto_id FROM producto WHERE producto_id = %s", (id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"status": "error", "message": "Producto no encontrado"}), 404

        query = "UPDATE producto SET nombre=%s, categoria=%s, precio=%s, stock=%s, descripcion=%s WHERE producto_id=%s"
        values = (data['nombre'], data['categoria'], data['precio'], data['stock'], descripcion, id)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "Registro actualizado correctamente"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 5. DELETE
@app.route('/api/v1/producto/<int:id>', methods=['DELETE'])
def delete_producto(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT producto_id FROM producto WHERE producto_id = %s", (id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"status": "error", "message": "Producto no encontrado"}), 404

        cursor.execute("DELETE FROM producto WHERE producto_id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "Registro eliminado exitosamente"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
