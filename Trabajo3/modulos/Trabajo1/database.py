"""
Configuración y manejo de base de datos
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Instancia global de SQLAlchemy
db = SQLAlchemy()

def initialize_database(app):
    """Inicializar la base de datos con la aplicación Flask"""
    db.init_app(app)

    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        print("✅ Base de datos inicializada correctamente")

class BaseModel(db.Model):
    """Modelo base con campos comunes"""
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convertir modelo a diccionario"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def save(self):
        """Guardar el modelo en la base de datos"""
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """Eliminar el modelo de la base de datos"""
        db.session.delete(self)
        db.session.commit()
