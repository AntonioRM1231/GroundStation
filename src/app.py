from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'web_sockets'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/estacion_prueba'
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

class Mission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), nullable=False)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())
    lugar = db.Column(db.String(30), nullable=False)
    id_vehiculo = db.Column(db.Integer, db.ForeignKey('vehiculo.id'), nullable=False)

    vehiculo = db.relationship('Vehiculo', backref=db.backref('misiones', lazy=True))


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






# ---- FORMULARIO PARA AGREGAR MISIÓN ----
@app.route('/add_mission', methods=['GET', 'POST'])
def add_mission():
    vehiculos = Vehiculo.query.all()  # Para el combobox

    if request.method == 'POST':
        nombre = request.form['nombre']
        lugar = request.form['lugar']
        id_vehiculo = request.form['id_vehiculo']

        nueva_mision = Mission(
            nombre=nombre,
            lugar=lugar,
            id_vehiculo=id_vehiculo
        )
        db.session.add(nueva_mision)
        db.session.commit()

        # En lugar de redirect, mostramos mensaje y luego redirigimos
        return render_template('success_redirect.html',
                               mensaje="✅ Misión añadida correctamente",
                               destino=url_for('graficas_admin'))

    return render_template('add_mission.html', vehiculos=vehiculos)




@app.route('/show_mission')
def show_mission():
    misiones = Mission.query.all()
    return render_template('show_mission.html', misiones=misiones)



@app.route('/graficas_admin')
def graficas_admin():
    return render_template('graficas_admin.html')




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
