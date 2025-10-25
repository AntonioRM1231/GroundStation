from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send 

app = Flask(__name__)
#Clave secreta para websockets
app.config['SECRET_KEY'] = 'web_sockets'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('graficas.html')

@app.route('/connect')
def connect():
    return render_template('connect.html')


@socketio.on('telemetria')
def telemetria(trama):
    print(trama)
    event_name = 'telemetria'
    emit(event_name,trama, broadcast=True)

if __name__ == '__main__':
    #Usar '0.0.0.0' para que sea accesible en la red local 
    app.run(debug=True)
    #socketio.run(app, debug=True, host='0.0.0.0', port=5000)