"""
¡Aquí definimos la configuración de Remington Song API! ⚙️
Podemos tener diferentes configuraciones para desarrollo, pruebas y producción.
"""
import os
from datetime import timedelta

class Config:
    """
    Configuración base para Remington Song API.
    """
    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///remington_song.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desactivamos el tracking de modificaciones

    # Configuración de seguridad
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'remington_song_clave_secreta_muy_segura'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'remington_song_jwt_clave_secreta_muy_segura'  # Clave secreta para JWT
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Tiempo de expiración del token

    # Configuración adicional
    DEBUG = False  # Modo debug desactivado por defecto

class DevelopmentConfig(Config):
    """
    Configuración para el entorno de desarrollo de Remington Song.
    """
    DEBUG = True  # Activamos el modo debug
    SQLALCHEMY_ECHO = True  # Mostramos las consultas SQL en la consola

class TestingConfig(Config):
    """
    Configuración para el entorno de pruebas de Remington Song.
    """
    TESTING = True  # Activamos el modo de pruebas
    SQLALCHEMY_DATABASE_URI = 'sqlite://