from flask import Flask, jsonify, request, render_template
import mysql.connector

app = Flask(__name__)

# Configuración de conexión a la base de datos
db_config = {
    'host': 'localhost',
    'user': 'perez',
    'password': 'perez123',  
    'database': 'techgear_db'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)



# 1. RUTA HTML - INTERFAZ WEB (Primera Actividad)

@app.route('/', methods=['GET'])
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM producto")
        productos = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('index.html', productos=productos)
    except Exception as e:
        return f"Error al cargar la interfaz web: {str(e)}", 500



# 2. ENDPOINTS API RESTful - RESPUESTAS JSON (Actividad Actual)

# GET: Obtener todos los productos
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


# GET: Obtener un solo producto por ID
@app.route('/api/v1/producto/<int:producto_id>', methods=['GET'])
def get_producto_by_id(producto_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM producto WHERE producto_id = %s", (producto_id,))
        producto = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if producto:
            return jsonify(producto), 200
        else:
            return jsonify({"status": "error", "message": "Producto no encontrado"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# POST: Crear un nuevo producto
@app.route('/api/v1/producto', methods=['POST'])
def create_producto():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "JSON body requerido"}), 400

        nombre = data.get('nombre')
        categoria = data.get('categoria')
        precio = data.get('precio')
        stock = data.get('stock')
        descripcion = data.get('descripcion')

        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO producto (nombre, categoria, precio, stock, descripcion)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (nombre, categoria, precio, stock, descripcion))
        conn.commit()
        nuevo_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "Registro creado exitosamente",
            "id": nuevo_id
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# PUT: Actualizar un producto existente
@app.route('/api/v1/producto/<int:producto_id>', methods=['PUT'])
def update_producto(producto_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "JSON body requerido"}), 400

        nombre = data.get('nombre')
        categoria = data.get('categoria')
        precio = data.get('precio')
        stock = data.get('stock')
        descripcion = data.get('descripcion')

        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si el registro existe
        cursor.execute("SELECT producto_id FROM producto WHERE producto_id = %s", (producto_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"status": "error", "message": "Producto no encontrado"}), 404

        query = """
            UPDATE producto
            SET nombre = %s, categoria = %s, precio = %s, stock = %s, descripcion = %s
            WHERE producto_id = %s
        """
        cursor.execute(query, (nombre, categoria, precio, stock, descripcion, producto_id))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "Registro actualizado correctamente"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# DELETE: Eliminar un producto
@app.route('/api/v1/producto/<int:producto_id>', methods=['DELETE'])
def delete_producto(producto_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si el registro existe
        cursor.execute("SELECT producto_id FROM producto WHERE producto_id = %s", (producto_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"status": "error", "message": "Producto no encontrado"}), 404

        cursor.execute("DELETE FROM producto WHERE producto_id = %s", (producto_id,))
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
