"""
Configuraciones del sistema VideoStream API
Soporte para múltiples entornos
"""

import os
from datetime import timedelta

class BaseConfig:
    """Configuración base compartida"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'videostream-secret-key-2024'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False

    # Configuración de paginación
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100

class DevelopmentConfig(BaseConfig):
    """Configuración para desarrollo"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///videostream_dev.db'
    SQLALCHEMY_ECHO = True  # Log de queries SQL

class ProductionConfig(BaseConfig):
    """Configuración para producción"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///videostream_prod.db'

class TestingConfig(BaseConfig):
    """Configuración para testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Mapeo de configuraciones
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
