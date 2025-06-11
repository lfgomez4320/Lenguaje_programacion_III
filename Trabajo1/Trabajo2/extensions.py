"""
¡Aquí definimos las extensiones que usaremos en Remington Song API! 🔌
Esto nos permite mantener el código más limpio y organizado.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# Creamos las instancias de las extensiones
db = SQLAlchemy()  # Para interactuar con la base de datos
migrate = Migrate()  # Para gestionar las migraciones de la base de datos
jwt = JWTManager()  # Para la autenticación con JWT