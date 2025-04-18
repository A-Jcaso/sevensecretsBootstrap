from flask import Flask, render_template
from models import Services
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

if __name__=='__main__':
    app.run(debug = True) 