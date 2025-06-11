"""
¡Aquí definimos nuestros modelos de datos para Remington Song! 📚
Estos modelos representan las tablas de nuestra base de datos.
"""
from .extensions import db  # Importamos la instancia de SQLAlchemy
from datetime import datetime

class Usuario(db.Model):
    """
    Modelo para los usuarios de Remington Song.
    """
    __tablename__ = 'usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contraseña = db.Column(db.String(128), nullable=False)  # Campo de contraseña
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relación con favoritos
    favoritos = db.relationship('Favorito', backref='usuario', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Usuario {self.nombre}>'
    
    def to_dict(self):
        """Convierte el usuario a diccionario (sin contraseña)"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'correo': self.correo,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None
        }

class Cancion(db.Model):
    """
    Modelo para las canciones de Remington Song.
    """
    __tablename__ = 'cancion'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    artista = db.Column(db.String(100), nullable=False)
    album = db.Column(db.String(100))
    duracion = db.Column(db.Integer)  # Duración en segundos
    año = db.Column(db.Integer)
    genero = db.Column(db.String(50))
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relación con favoritos
    favoritos = db.relationship('Favorito', backref='cancion', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Cancion {self.titulo} - {self.artista}>'
    
    def to_dict(self):
        """Convierte la canción a diccionario"""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'artista': self.artista,
            'album': self.album,
            'duracion': self.duracion,
            'año': self.año,
            'genero': self.genero,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }

class Favorito(db.Model):
    """
    Modelo para la relación de favoritos entre usuarios y canciones en Remington Song.
    """
    __tablename__ = 'favorito'
    
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_cancion = db.Column(db.Integer, db.ForeignKey('cancion.id'), nullable=False)
    fecha_marcado = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Constraint único para evitar duplicados
    __table_args__ = (db.UniqueConstraint('id_usuario', 'id_cancion', name='unique_user_song_favorite'),)

    def __repr__(self):
        return f'<Favorito Usuario:{self.id_usuario} Cancion:{self.id_cancion}>'
    
    def to_dict(self):
        """Convierte el favorito a diccionario"""
        return {
            'id': self.id,
            'id_usuario': self.id_usuario,
            'id_cancion': self.id_cancion,
            'fecha_marcado': self.fecha_marcado.isoformat() if self.fecha_marcado else None
        }