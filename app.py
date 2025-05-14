from flask import Flask, render_template, redirect, url_for, request, flash
from models import Services
from send_email import send_email as send_email_function
import sqlite3

conexion = sqlite3.connect("sevensecrets_db.db",
                           check_same_thread=False)

app = Flask(__name__)
app.secret_key = '1234'

@app.route("/") 
def home():
    services = Services.get_all(conexion)
    return render_template("home.html", data = {
        "services":services
    })

@app.route("/detail<int:service_id>")
def service_detail (service_id):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM services WHERE id = ?", (service_id,))
    row = cursor.fetchone()

    if row:
        service = Services(row[0], row[1], row[2], row[3], row[4])
        return render_template("detail.html", service=service)
    else:
        return "Servicio no encontrado", 404

@app.route("/booking")
def booking():
        return render_template("booking.html")

@app.route('/send-email', methods=['POST']) 
def send_email():
    if request.method == 'POST':
        nombre_cliente = request.form['nombreCliente']
        apellido_cliente = request.form['apellidoCliente']
        celular_cliente = request.form['numero_celular']
        email = request.form['email']
        subject = "Mensaje de: " + nombre_cliente + " " + apellido_cliente + " | Correo: " + email + " | Número de celular: " + celular_cliente
        body = request.form['mensaje1']
        send_email_function(subject, body)
    return redirect(url_for('booking'))

@app.route("/contacts") 
def contacts():
    return render_template("contacts.html")

#####Nuevo tratamiento
@app.route('/templates/form_tratamiento', methods=['GET'])
def nuevo_tratamiento():
    return render_template('form_tratamiento.html')

# Ruta para procesar el formulario
@app.route('/templates/form_tratamiento', methods=['POST'])
def crear_tratamiento():
    nombre = request.form.get('nombreTratamiento')
    descripcion = request.form.get('descripcion')
    img = request.form.get('imagen')

    # Mostrar en la terminal los datos recibidos
    print(f"Nombre: {nombre}")
    print(f"Descripcion: {descripcion}")
    print(f"Imagen: {img}")

    flash('Tratamiento registrado correctamente')
    return redirect(url_for('nuevo_tratamiento'))

######Nuevo cliente
@app.route('/templates/form_clientes', methods=['GET'])
def nuevo_cliente():
    return render_template('form_clientes.html')

# Ruta para procesar el formulario
@app.route('/templates/form_clientes', methods=['POST'])
def crear_cliente():
    nombre = request.form.get('nombreCliente')
    apellido = request.form.get('apellidoCliente')
    celular = request.form.get('numero_celular')
    email = request.form.get('email')

    # Mostrar en la terminal los datos recibidos
    print(f"Nombre: {nombre}")
    print(f"Apellido: {apellido}")
    print(f"Celular: {celular}")
    print(f"Email: {email}")

    flash(f'Cliente registrado correctamente. Nombre {nombre} y apellido {apellido}')
    return redirect(url_for('nuevo_cliente'))

#####Nuevo personal
@app.route('/templates/form_personal', methods=['GET'])
def nuevo_personal():
    return render_template('form_personal.html')

# Ruta para procesar el formulario
@app.route('/templates/form_personal', methods=['POST'])
def crear_personal():
    nombre = request.form.get('nombrePersonal')
    apellido = request.form.get('apellidoPersonal')
    celular = request.form.get('numero_celular')
    email = request.form.get('email')
    cargo = request.form.get('cargo')

    # Mostrar en la terminal los datos recibidos
    print(f"Nombre: {nombre}")
    print(f"Precio: {apellido}")
    print(f"Celular: {celular}")
    print(f"Email: {email}")   
    print(f"Cargo: {cargo}")
    
    flash(f'Trabajador registrado correctamente. Nombre {nombre} y apellido {apellido}')
    return redirect(url_for('nuevo_personal'))

if __name__=='__main__':
    app.run(debug = True) 
    
    