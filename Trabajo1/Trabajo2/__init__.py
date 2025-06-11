"""
¡Este es el corazón de nuestra API de Música: Remington Song! 🎵
Aquí definimos la función create_app, que inicializa y configura la aplicación Flask.
"""
from flask import Flask
from flask_restx import Api
from .config import Config  # Importamos la configuración base
from .extensions import db, migrate, jwt  # Importamos las extensiones
from .resources import api as ns1  # Importamos el namespace de recursos
from .models import Usuario, Cancion, Favorito  # Importamos los modelos
from flask_cors import CORS  # Importamos CORS

def create_app(config_class=Config):
    """
    Crea y configura la aplicación Flask para Remington Song.

    Args:
        config_class: La clase de configuración a utilizar (por defecto, Config).

    Returns:
        Una instancia de la aplicación Flask.
    """
    # Creamos la aplicación Flask
    app = Flask(__name__)

    # Cargamos la configuración desde la clase config_class
    app.config.from_object(config_class)

    # Inicializamos las extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)  # Inicializamos JWT
    CORS(app)  # Habilitamos CORS

    # Creamos la API de Flask-RESTx
    api = Api(
        app,
        version='1.0',
        title='Remington Song API',
        description='Una API RESTful para gestionar usuarios, canciones y favoritos en Remington Song.',
        doc='/docs'  # Endpoint para la documentación Swagger
    )

    # Agregamos el namespace de recursos a la API
    api.add_namespace(ns1)

    # Registramos un hook para crear la base de datos si no existe
    @app.before_first_request
    def create_tables():
        db.create_all()
        print("🎵 Base de datos de Remington Song inicializada correctamente")

    return app