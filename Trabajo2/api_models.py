"""
¡Aquí definimos los modelos de la API para Flask-RESTx en Remington Song! 🎨
Estos modelos nos ayudan a definir cómo se ven los datos que enviamos y recibimos en la API.
"""
from flask_restx import fields

# Modelo para la representación de un usuario en la API
usuario_model = {
    'id': fields.Integer(description='Identificador único del usuario'),
    'nombre': fields.String(required=True, description='Nombre del usuario'),
    'correo': fields.String(required=True, description='Correo electrónico del usuario'),
    'fecha_registro': fields.DateTime(description='Fecha de registro del usuario')
}

# Modelo para la representación de una canción en la API
cancion_model = {
    'id': fields.Integer(description='Identificador único de la canción'),
    'titulo': fields.String(required=True, description='Título de la canción'),
    'artista': fields.String(required=True, description='Artista de la canción'),
    'album': fields.String(description='Álbum de la canción'),
    'duracion': fields.Integer(description='Duración de la canción en segundos'),
    'año': fields.Integer(description='Año de lanzamiento de la canción'),
    'genero': fields.String(description='Género de la canción'),
    'fecha_creacion': fields.DateTime(description='Fecha de creación de la canción')
}

# Modelo para la representación de un favorito en la API
favorito_model = {
    'id': fields.Integer(description='Identificador único del favorito'),
    'id_usuario': fields.Integer(required=True, description='Identificador del usuario'),
    'id_cancion': fields.Integer(required=True, description='Identificador de la canción'),
    'fecha_marcado': fields.DateTime(description='Fecha en que se marcó como favorito')
}

# Modelo para la autenticación
auth_model = {
    'correo': fields.String(required=True, description='Correo electrónico del usuario'),
    'contraseña': fields.String(required=True, description='Contraseña del usuario')
}

# Modelo para el token de acceso
token_model = {
    'access_token': fields.String(description='Token de acceso JWT'),
    'message': fields.String(description='Mensaje de confirmación')
}

# Modelo para registro de usuario
registro_model = {
    'nombre': fields.String(required=True, description='Nombre del usuario'),
    'correo': fields.String(required=True, description='Correo electrónico del usuario'),
    'contraseña': fields.String(required=True, description='Contraseña del usuario')
}

# Modelo para búsqueda de canciones
busqueda_model = {
    'titulo': fields.String(description='Título de la canción a buscar'),
    'artista': fields.String(description='Artista de la canción a buscar'),
    'genero': fields.String(description='Género de la canción a buscar')
}