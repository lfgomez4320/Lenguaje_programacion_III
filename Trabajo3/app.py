from flask import Flask, render_template, request
import requests

# Importa las funciones que necesitas de cada trabajo
from modulos.Trabajo1.app import mi_funcion
from modulos.Trabajo2.app import otra_funcion

app = Flask(__name__)

# URL base del API lp3-taller2 (reemplaza con la URL real)
API_BASE_URL = "http://api.example.com"

@app.route('/')
def index():
    # Ejemplo de cómo consumir el API
    try:
        response = requests.get(f"{API_BASE_URL}/endpoint")
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        data = {"error": str(e)}

    # Llama a funciones de tus módulos
    resultado_trabajo1 = mi_funcion()
    resultado_trabajo2 = otra_funcion()

    return render_template('index.html', 
                           data=data,
                           resultado_trabajo1=resultado_trabajo1,
                           resultado_trabajo2=resultado_trabajo2)

if __name__ == '__main__':
    app.run(debug=True)