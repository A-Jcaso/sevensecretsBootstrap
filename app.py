from flask import Flask, render_template, redirect, url_for, request
from models import Services
from send_email import send_email as send_email_function
import sqlite3

conexion = sqlite3.connect("sevensecrets_db.db",
                           check_same_thread=False)

app = Flask(__name__)

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

if __name__=='__main__':
    app.run(debug = True) 
    
    