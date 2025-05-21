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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ahsedlik_myuser:70077307hs@mysql-ahsedlik.alwaysdata.net/ahsedlik_mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define a model (table) in MySQL
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    apellido = db.Column(db.String(120), unique=True, nullable=False)
    celular = db.Column(db.String(120), unique=True, nullable=False)
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

# Route to add a new user
@app.route('/add', methods=['GET'])
def add_user():
    import random
    random_number = random.randint(10, 1000)

    username = str(random_number) + "user"
    email = str(random_number) + "user@gmail.com"
    new_user = haro(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/')

######Nuevo cliente
@app.route('/templates/form_clientes', methods=['GET'])
def nuevo_cliente():
    nombre = request.form.get('nombreCliente')
    apellido = request.form.get('apellidoCliente')
    celular = request.form.get('numero_celular')
    email = request.form.get('email')
    new_user = Cliente(username=nombre,apellido = apellido,celular=celular, email=email)
    db.session.add(new_user)
    db.session.commit()
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




    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)