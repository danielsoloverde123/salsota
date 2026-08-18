import os
from flask import Flask, render_template, request, flash, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Configuración de Flask
app.secret_key = os.environ.get('SECRET_KEY', 'elbulevar_salsa_clave_secreta_2026')

# Configuración directa de MySQL
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_USER = os.environ.get('MYSQL_USER', 'bulevar')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'bulevar123')
MYSQL_DB = os.environ.get('MYSQL_DB', 'elbulevar_db')
MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))

def obtener_conexion_db():
    """Establece y retorna la conexión con la base de datos MySQL."""
    try:
        conexion = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            port=MYSQL_PORT
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"Error de conexión a MySQL: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/historia')
def historia():
    return render_template('historia.html')

@app.route('/sobre-nosotros')
def sobre_nosotros():
    return render_template('sobre_nosotros.html')

@app.route('/contactenos', methods=['GET', 'POST'])
def contactenos():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip()
        asunto = request.form.get('asunto', '').strip()
        mensaje = request.form.get('mensaje', '').strip()

        # Validación del lado del servidor
        if not nombre or not email or not asunto or not mensaje:
            flash('Todos los campos son obligatorios. Por favor, llene el formulario.', 'danger')
            return redirect(url_for('contactenos'))

        if len(nombre) < 3:
            flash('El nombre debe tener al menos 3 caracteres.', 'danger')
            return redirect(url_for('contactenos'))

        if '@' not in email or '.' not in email:
            flash('Por favor ingrese un correo electrónico válido.', 'danger')
            return redirect(url_for('contactenos'))

        # Guardado en la base de datos
        conexion = obtener_conexion_db()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = "INSERT INTO contactos (nombre, email, asunto, mensaje) VALUES (%s, %s, %s, %s)"
                valores = (nombre, email, asunto, mensaje)
                cursor.execute(sql, valores)
                conexion.commit()
                cursor.close()
                conexion.close()
                flash('¡Tu mensaje ha sido recibido con éxito en ELBULEVAR! Pronto nos pondremos en contacto contigo.', 'success')
            except Error as e:
                print(f"Error en la consulta MySQL: {e}")
                flash('Ocurrió un error interno al intentar guardar tu mensaje. Por favor intenta más tarde.', 'danger')
        else:
            flash('No fue posible conectar con la base de datos de ELBULEVAR.', 'danger')

        return redirect(url_for('contactenos'))

    return render_template('contactenos.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)