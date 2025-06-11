"""
¡Aquí arranca nuestra increíble API de Música: Remington Song! 🎶
Este script se encarga de configurar y poner en marcha la aplicación Flask.
"""
import os
from remington_song import create_app  # Importamos nuestra "fábrica" de apps
from dotenv import load_dotenv  # Para cargar las variables de entorno

# Cargamos las variables de entorno desde el archivo .env (si existe)
# Esto es útil para configurar la app sin modificar el código
load_dotenv()

# Creamos la aplicación utilizando la función create_app de nuestro paquete remington_song
app = create_app()

if __name__ == "__main__":
    # Obtenemos el puerto del entorno, o usamos el 5000 por defecto
    # Esto permite que la app se ejecute en diferentes entornos (local, producción, etc.)
    port = int(os.environ.get("PORT", 5000))

    # Verificamos si estamos en modo debug (útil para desarrollo)
    # Si la variable FLASK_DEBUG está en 1, activamos el modo debug
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"

    # ¡Ponemos en marcha la aplicación!
    # Usamos host="0.0.0.0" para que sea accesible desde cualquier IP
    print("🎵 Iniciando Remington Song API...")
    print(f"🚀 Servidor disponible en: http://localhost:{port}")
    print("📖 Documentación Swagger en: http://localhost:{}/docs".format(port))
    app.run(host="0.0.0.0", port=port, debug=debug)