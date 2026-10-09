from flask import Flask, render_template
from db import get_db_connection
from api.modulos.productos import productos_bp
from api.modulos.clientes import clientes_bp

app = Flask(__name__)

# Registrar Blueprints de la API
app.register_blueprint(productos_bp)
app.register_blueprint(clientes_bp)

# RUTA HTML - INTERFAZ WEB
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)