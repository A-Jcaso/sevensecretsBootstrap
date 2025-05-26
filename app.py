from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import Services
from send_email import send_email as send_email_function
import sqlite3

conexion = sqlite3.connect("sevensecrets_db.db",
                           check_same_thread=False)

app = Flask(__name__)
app.secret_key = '1234'

# MySQL configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ahsedlik_myuser:70077307hs@mysql-ahsedlik.alwaysdata.net/ahsedlik_seven_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define a model (table) in MySQL
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cli_nombre = db.Column(db.String(80), unique=False, nullable=False)
    cli_apellido = db.Column(db.String(120), unique=False, nullable=False)
    cli_dni = db.Column(db.String(120), unique=True, nullable=False)
    cli_email = db.Column(db.String(120), unique=True, nullable=False)
    cli_celular = db.Column(db.String(120), unique=True, nullable=False)
    def __repr__(self):
        return f'<User {self.username}>'

class Personal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    per_nombre = db.Column(db.String(80), unique=False, nullable=False)
    per_apellido = db.Column(db.String(120), unique=False, nullable=False)
    per_dni = db.Column(db.String(120), unique=True, nullable=False)
    per_email = db.Column(db.String(120), unique=True, nullable=False)
    per_celular = db.Column(db.String(120), unique=True, nullable=False)
    per_cargo = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
    
class Tratamiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tra_nombre = db.Column(db.String(80), unique=False, nullable=False)
    tra_descripcion = db.Column(db.String(120), unique=False, nullable=False)
    tra_imagen = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

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

################Nuevo tratamiento###################################
@app.route('/templates/form_tratamiento', methods=['GET'])
def nuevo_tratamiento():
    return render_template('form_tratamiento.html')

# Ruta para procesar el formulario
@app.route('/templates/form_tratamiento', methods=['POST'])
def crear_tratamiento():
    nombre = request.form.get('nombreTratamiento')
    descripcion = request.form.get('descripcion')
    img = request.form.get('imagen')

    if not nombre or not descripcion or not img:
        flash("Todos los campos son obligatorios")
        return redirect(url_for('nuevo_tratamiento'))
    
    new_tratamiento = Tratamiento(tra_nombre=nombre, tra_descripcion=descripcion, tra_imagen=img)
    db.session.add(new_tratamiento)
    db.session.commit()
    
    # Mostrar en la terminal los datos recibidos
    print(f"Nombre: {nombre}")
    print(f"Descripcion: {descripcion}")
    print(f"Imagen link: {img}")

    flash('Tratamiento registrado correctamente')
    return redirect(url_for('nuevo_tratamiento'))

########################Nuevo cliente####################################

@app.route('/templates/form_clientes', methods=['GET'])
def nuevo_cliente():
    return render_template('form_clientes.html')

# Ruta para procesar el formulario
@app.route('/templates/form_clientes', methods=['POST'])
def crear_cliente():
    nombre = request.form.get('nombreCliente')
    apellido = request.form.get('apellidoCliente')
    dni = request.form.get('dni')
    celular = request.form.get('numero_celular')
    email = request.form.get('email')

    if not nombre or not apellido or not celular or not email:
        flash("Todos los campos son obligatorios")
        return redirect(url_for('nuevo_cliente'))

    new_user = Cliente(cli_nombre=nombre, cli_apellido=apellido, cli_dni=dni, cli_celular=celular, cli_email=email)
    db.session.add(new_user)
    db.session.commit()
    
    # Mostrar en la terminal los datos recibidos
    print(f"Nombre: {nombre}")
    print(f"Apellido: {apellido}")
    print(f"DNI: {dni}")
    print(f"Celular: {celular}")
    print(f"Email: {email}")

    flash(f'Cliente registrado correctamente. Nombre {nombre} y apellido {apellido}')
    return redirect(url_for('nuevo_cliente'))

########################Nuevo personal######################################

@app.route('/templates/form_personal', methods=['GET'])
def nuevo_personal():
    return render_template('form_personal.html')

# Ruta para procesar el formulario
@app.route('/templates/form_personal', methods=['POST'])
def crear_personal():
    nombre = request.form.get('nombrePersonal')
    apellido = request.form.get('apellidoPersonal')
    dni = request.form.get('dni')
    celular = request.form.get('numero_celular')
    email = request.form.get('email')
    cargo = request.form.get('cargo')

    # Mostrar en la terminal los datos recibidos
    print(f"Nombre: {nombre}")
    print(f"Apellido: {apellido}")
    print(f"DNI: {dni}")
    print(f"Celular: {celular}")
    print(f"Email: {email}")   
    print(f"Cargo: {cargo}")
    
    if not nombre or not apellido or not dni or not celular or not email or not cargo:
        flash("Todos los campos son obligatorios")
        return redirect(url_for('nuevo_personal'))

    new_staff = Personal(per_nombre=nombre, per_apellido=apellido,per_dni=dni, per_celular=celular, per_email=email, per_cargo=cargo)
    db.session.add(new_staff)
    db.session.commit()
    
    flash(f'Trabajador registrado correctamente. Nombre {nombre} y apellido {apellido}')
    return redirect(url_for('nuevo_personal'))
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)