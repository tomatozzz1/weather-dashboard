import os 
from flask import Flask, render_template, jsonify, request
from weather_service import ServicioClima
import webbrowser
from threading import Timer

app = Flask(__name__)
servicio = ServicioClima()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/clima')
def api_clima():
    ciudad = request.args.get('ciudad', 'Guadalajara')
    datos = servicio.obtener_datos_tablero(ciudad)
    return jsonify(datos)

if __name__ == '__main__':
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        def abrir_navegador():
            webbrowser.open_new("http://127.0.0.1:5000")
        
        Timer(1, abrir_navegador).start()

    app.run(debug=True, host='0.0.0.0', port=5000)