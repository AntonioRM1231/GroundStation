from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'web_sockets'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/Estacion_vuelo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

socketio = SocketIO(app)
db = SQLAlchemy(app)

# ======================
# MODELO DE VEHÍCULO
# ======================
class Vehiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)

# ======================
# RUTAS
# ======================

@app.route('/')
def index():
    return render_template('graficas.html')

@app.route('/connect')
def connect():
    return render_template('connect.html')

# ---- FORMULARIO PARA AGREGAR VEHÍCULO ----
@app.route('/add_vehicle', methods=['GET', 'POST'])
def add_vehicle():
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        tipo = request.form['tipo']

        nuevo = Vehiculo(nombre=nombre, categoria=categoria, tipo=tipo)
        db.session.add(nuevo)
        db.session.commit()

        return redirect(url_for('show_vehicles'))
    return render_template('add_vehicle.html')

# ---- MOSTRAR VEHÍCULOS ----
@app.route('/show_vehicles')
def show_vehicles():
    vehiculos = Vehiculo.query.all()
    return render_template('show_vehicles.html', vehiculos=vehiculos)

# ======================
# SOCKETS
# ======================
@socketio.on('telemetria')
def telemetria(trama):
    print('Trama recibida:', trama)
    emit('telemetria', trama, broadcast=True)

# ======================
# MAIN
# ======================
if __name__ == '__main__':
    import eventlet
    import eventlet.wsgi
    with app.app_context():
        db.create_all()  # Crea la tabla si no existe
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
