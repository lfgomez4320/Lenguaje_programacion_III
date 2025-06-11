"""
¡Aquí definimos los recursos de Remington Song API! 🚀
Los recursos son las clases que manejan las peticiones HTTP a nuestros endpoints.
"""
from flask import request
from flask_restx import Namespace, Resource, fields
from .extensions import db, jwt
from .models import Usuario, Cancion, Favorito
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy import or_

# Creamos un namespace para agrupar los recursos de la API
api = Namespace('api', description='Operaciones de Remington Song - Usuarios, canciones y favoritos')

# Importamos los modelos de la API
from .api_models import (
    usuario_model as um, cancion_model as cm, favorito_model as fm,
    auth_model as am, token_model as tm, registro_model as rm, busqueda_model as bm
)

usuario_model = api.model('Usuario', um)
cancion_model = api.model('Cancion', cm)
favorito_model = api.model('Favorito', fm)
auth_model = api.model('Auth', am)
token_model = api.model('Token', tm)
registro_model = api.model('Registro', rm)
busqueda_model = api.model('Busqueda', bm)

# Definimos el modelo para la creación/actualización de un usuario
usuario_input = api.model('UsuarioInput', {
    'nombre': fields.String(required=True, description='Nombre del usuario'),
    'correo': fields.String(required=True, description='Correo electrónico del usuario'),
    'contraseña': fields.String(required=True, description='Contraseña del usuario')
})

# Definimos el modelo para la creación/actualización de una canción
cancion_input = api.model('CancionInput', {
    'titulo': fields.String(required=True, description='Título de la canción'),
    'artista': fields.String(required=True, description='Artista de la canción'),
    'album': fields.String(description='Álbum de la canción'),
    'duracion': fields.Integer(description='Duración de la canción en segundos'),
    'año': fields.Integer(description='Año de lanzamiento de la canción'),
    'genero': fields.String(description='Género de la canción')
})

# Modelo para crear favoritos
favorito_input = api.model('FavoritoInput', {
    'id_usuario': fields.Integer(required=True, description='ID del usuario'),
    'id_cancion': fields.Integer(required=True, description='ID de la canción')
})

# ----------------------------------------------------------------------------------------------------
# Recursos para Autenticación
# ----------------------------------------------------------------------------------------------------
@api.route('/auth/register')
class Registro(Resource):
    """
    Recurso para registrar un nuevo usuario en Remington Song.
    """
    @api.doc(description='Registrar un nuevo usuario en Remington Song')
    @api.expect(registro_model)
    @api.marshal_with(usuario_model, code=201)
    def post(self):
        """
        Registrar un nuevo usuario en Remington Song.
        """
        try:
            data = request.get_json()
            correo = data['correo']
            contraseña = data['contraseña']
            nombre = data['nombre']

            # Verificar si el usuario ya existe
            if Usuario.query.filter_by(correo=correo).first():
                api.abort(409, f"El correo '{correo}' ya está registrado en Remington Song.")

            # Hash de la contraseña antes de guardarla
            hashed_password = generate_password_hash(contraseña)

            nuevo_usuario = Usuario(
                nombre=nombre,
                correo=correo,
                contraseña=hashed_password,
                fecha_registro=datetime.utcnow()
            )
            db.session.add(nuevo_usuario)
            db.session.commit()
            
            return nuevo_usuario.to_dict(), 201
        except Exception as e:
            api.abort(500, f"Error interno del servidor: {str(e)}")

@api.route('/auth/login')
class Login(Resource):
    """
    Recurso para iniciar sesión en Remington Song y obtener un token de acceso.
    """
    @api.doc(description='Iniciar sesión en Remington Song y obtener un token de acceso')
    @api.expect(auth_model)
    @api.marshal_with(token_model)
    def post(self):
        """
        Iniciar sesión en Remington Song y obtener un token de acceso.
        """
        try:
            data = request.get_json()
            correo = data['correo']
            contraseña = data['contraseña']

            usuario = Usuario.query.filter_by(correo=correo).first()

            if not usuario or not check_password_hash(usuario.contraseña, contraseña):
                api.abort(401, "Credenciales inválidas para Remington Song.")

            access_token = create_access_token(identity=correo)
            return {
                'access_token': access_token,
                'message': f'¡Bienvenido a Remington Song, {usuario.nombre}!'
            }
        except Exception as e:
            api.abort(500, f"Error interno del servidor: {str(e)}")

# ----------------------------------------------------------------------------------------------------
# Recursos para Usuarios
# ----------------------------------------------------------------------------------------------------
@api.route('/usuarios')
class UsuarioList(Resource):
    """
    Recurso para listar y crear usuarios en Remington Song.
    """
    @api.doc(description='Listar todos los usuarios de Remington Song')
    @api.marshal_list_with(usuario_model)
    @jwt_required()
    def get(self):
        """
        Listar todos los usuarios de Remington Song.
        """
        try:
            usuarios = Usuario.query.all()
            return [usuario.to_dict() for usuario in usuarios]
        except Exception as e:
            api.abort(500, f"Error interno del servidor: {str(e)}")

    @api.doc(description='Crear un nuevo usuario en Remington Song')
    @api.expect(usuario_input)
    @api.marshal_with(usuario_model)
    def post(self):
        """
        Crear un nuevo usuario en Remington Song.
        """
        try:
            data = request.get_json()
            
            # Verificar si el usuario ya existe
            if Usuario.query.filter_by(correo=data['correo']).first():
                api.abort(409, f"El correo '{data['correo']}' ya está registrado.")
            
            # Hash de la contraseña antes de guardarla
            hashed_password = generate_password_hash(data['contraseña'])
            
            nuevo_usuario = Usuario(
                nombre=data['nombre'],
                correo=data['correo'],
                contraseña=hashed_password,
                fecha_registro=datetime.utcnow()
            )
            db.session.add(nuevo_usuario)
            db.session.commit()
            
            return nuevo_usuario.to_dict(), 201
        except Exception as e:
            api.abort(500, f"Error interno del servidor: {str(e)}")

@api.route('/usuarios/<int:id>')
class UsuarioResource(Resource):
    """
    Recurso para obtener, actualizar y eliminar un usuario específico.
    """
    @api.doc(description='Obtener un usuario por su ID')
    @api.marshal_with(usuario_model)
    @jwt_required()
    def get(self, id):
        """
        Obtener un usuario por su ID.
        """
        try:
            usuario = Usuario.query.get_or_404(id)
            return usuario.to_dict()
        except Exception as e:
            api.abort(500, f"Error interno del servidor: {str(e)}")

    @api.doc(description='Actualizar un usuario por su ID')
    @api.expect(usuario_input)
    @api.marshal_with(usuario_model)
    @jwt_required()
    def put(self, id):
        """
        Actualizar un usuario por su ID.
        """
        try:
            usuario = Usuario.query.get_or_404(id)
            data = request.get_json()
            
            usuario.nombre = data['nombre']
            usuario.correo = data['correo']
            
            # Hash de la contraseña antes de guardarla si se proporciona una nueva contraseña
            if 'contraseña' in data:
                usuario.contraseña = generate_password_hash(data['contraseña'])
            
            db.session.commit()
            return usuario.to_dict()
        except Exception as e:
            api.abort(500, f"Error interno del servidor: {str(e)}")

    @api.doc(description='Eliminar un usuario por su ID')
    @api.response(204, 'Usuario eliminado')
    @jwt_required()
    def delete(self, id):
        """
        Eliminar un usuario por su ID.
        """
        try:
            usuario = Usuario.query.get_or_404(id)
            db.session.delete(usuario)
            db.session.commit()
            return '', 204
        except Exception as e:
            api.abort(500, f"Error interno del servidor: {str(e)}")

# ----------------------------------------------------------------------------------------------------
# Recursos para Canciones
# ----------------------------------------------------------------------------------------------------
@api.route('/canciones')
class CancionList(Resource):
    """
    Recurso para listar y crear canciones en Remington Song.
    """
    @api.doc(description='Listar todas las canciones de Remington Song')
    @api.marshal_list_with(cancion_model)
    def get(self):
        """
        Listar todas las canciones de Remington Song.
        """
        try:
            canciones = Cancion.query.all()
            return [cancion.to_dict() for cancion in canciones]
        except Exception as e:
            api.abort(500, f"Error interno del servidor: {str(e)}")

    @api.doc(description='Crear una nueva canción en Remington Song')
    @api.expect(cancion_input)
    @api.marshal_with(cancion_model)
    def post(self):
        """
        Crear una nueva canción en Remington Song.
        """
        try:
            data = request.get_json()
            nueva_cancion = Cancion(
                titulo=data['titulo'],
                artista=data['artista'],
                album=data.get('album'),
                duracion=data.get('duracion'),
                año=data.get('año'),
                genero=data.get('genero'),
                fecha_creacion=datetime.utcnow()
            )
            db.session.add(nueva_cancion)
            db.session.commit()
            return nueva_cancion.to_dict(), 201
        except Exception as e:
            api.abort(500, f"Error interno del servidor: {str(e)}")

@api.route('/canciones/<int:id>')
class CancionResource(Resource):
    """
    Recurso para obtener, actualizar y eliminar una canción específica.
    """
    @api.doc(description='Obtener una canción por su ID')
    @api.marshal_with(cancion_model)
    def get(self, id):
        """
        Obtener una canción por su ID.
        """
        try:
            cancion = Cancion.query.get_or_404(id)
            return cancion.to_dict()
        except Exception as e:
            api.abort(500, f"Error interno del servidor: {str(e)}")

    @api.doc(description='Actualizar una canción por su ID')
    @api.expect(cancion_input)
    @api.marshal_with(cancion_model)
    def put(self, id):
        """
        Actualizar una canción por su ID.
        """
        try:
            cancion = Cancion.query.get_or_404(id)
            data = request.get_json()
            
            cancion.titulo = data['titulo']
            cancion.artista = data['artista']
            cancion.album = data.get('album')
            cancion.duracion = data.get('duracion')
            cancion.año = data.get('año')
            cancion.genero = data.get('genero')
            
            db.session.commit()
            return cancion.to_dict()
        except Exception as e:
            api.abort(500, f"Error interno del servidor: {str(e)}")

    @api.doc(description='Eliminar una canción por su ID')
    @api.response(204, 'Canción eliminada')
    def delete(self, id):
        """
        Eliminar una canción por su ID.
        """
        try:
            cancion = Cancion.query.get_or_404(id)
            db.session.delete(cancion)
            db.session.commit()
            return '', 204
        except Exception as e:
            api.abort(500, f"Error interno del servidor: {str(e)}")

@api.route('/canciones/buscar')
class CancionBuscar(Resource):
    """
    Recurso para buscar canciones en Remington Song.
    """
    @api.doc(description='Buscar canciones por título, artista o género')
    @api.expect(busqueda_model)
    @api.marshal_list_with(cancion_model)
    def get(self):
        """
        Buscar canciones por título, artista o género.
        """
        try:
            titulo = request.args.get('titulo', '')
            artista = request.args.get('artista', '')
            genero = request.args.get('genero', '')
            
            query = Cancion.query
            
            if titulo:
                query = query.filter(Cancion.titulo.contains(titulo))
            if artista:
                query = query.filter(Cancion.artista.contains(artista))
            if genero:
                query = query.filter(Cancion.genero.contains(genero))
            
            canciones = query.all()
            return [cancion.to_dict() for cancion in canciones]
        except Exception as e:
            api.abort(500, f"Error interno del servidor: {str(e)}")

# ----------------------------------------------------------------------------------------------------
# Recursos para Favoritos
# ----------------------------------------------------------------------------------------------------
@api.route('/favoritos')
class FavoritoList(Resource):
    """
    Recurso para listar y crear favoritos en Remington Song.
    """
    @api.doc(description='Listar todos los favoritos de Remington Song')
    @api.marshal_list_with(favorito_model)
    def get(self):
        """
        Listar todos los favoritos de Remington Song.
        """
        try:
            favoritos = Favorito.query.all()
            return [favorito.to_dict() for favorito in favoritos]
        except Exception as e:
            api.abort(500, f"Error interno del servidor: {str(e)}")

    @api.doc(description='Crear un nuevo favorito en Remington Song')
    @api.expect(favorito_input)
    @api.marshal_with(favorito_model)
    def post(self):
        """
        Crear un nuevo favorito en Remington Song.
        """
        try:
            data = request.get_json()
            
            # Verificar que no exista ya este favorito
            favorito_existente = Favorito.query.filter_by(
                id_usuario=data['id_usuario'],
                id_cancion=data['id_cancion']
            ).first()
            
            if favorito_existente:
                api.abort(409, "Esta canción ya está en los favoritos del usuario.")
            
            nuevo_favorito = Favorito(
                id_usuario=data['id_usuario'],
                id_cancion=data['id_cancion'],
                fecha_marcado=datetime.utcnow()
            )
            db.session.add(nuevo_favorito)
            db.session.commit()
            return nuevo_favorito.to_dict(), 201
        except Exception as e:
            api.abort(500, f"Error interno del servidor: {str(e)}")

@api.route('/favoritos/<int:id>')
class FavoritoResource(Resource):
    """
    Recurso para obtener y eliminar un favorito específico.
    """
    @api.doc(description='Obtener un favorito por su ID')
    @api.marshal_with(favorito_model)
    def get(self, id):
        """
        Obtener un favorito por su ID.
        """
        try:
            favorito = Favorito.query.get_or_404(id)
            return favorito.to_dict()
        except Exception as e:
            api.abort(500, f"Error interno del servidor: {str(e)}")

    @api.doc(description='Eliminar un favorito por su ID')
    @api.response(204, 'Favorito eliminado')
    def delete(self, id):
        """
        Eliminar un favorito por su ID.
        """
        try:
            favorito = Favorito.query.get_or_404(id)
            db.session.delete(favorito)
            db.session.commit()
            return '', 204
        except Exception as e:
            api.abort(500, f"Error interno del servidor: {str(e)}")

@api.route('/usuarios/<int:id>/favoritos')
class UsuarioFavoritosList(Resource):
    """
    Recurso para listar los favoritos de un usuario específico.
    """
    @api.doc(description='Listar los favoritos de un usuario')
    @api.marshal_list_with(favorito_model)
    def get(self, id):
        """
        Listar los favoritos de un usuario.
        """
        try:
            usuario = Usuario.query.get_or_404(id)
            return [favorito.to_dict() for favorito in usuario.favoritos]
        except Exception as e:
            api.abort(500, f"Error interno del servidor: {str(e)}")

@api.route('/usuarios/<int:id_usuario>/favoritos/<int:id_cancion>')
class UsuarioCancionFavoritoResource(Resource):
    """
    Recurso para marcar y desmarcar una canción como favorita para un usuario.
    """
    @api.doc(description='Marcar una canción como favorita para un usuario')
    @api.marshal_with(favorito_model)
    def post(self, id_usuario, id_cancion):
        """
        Marcar una canción como favorita para un usuario.
        """
        try:
            # Verificar que el usuario y la canción existan
            usuario = Usuario.query.get_or_404(id_usuario)
            cancion = Cancion.query.get_or_404(id_cancion)
            
            # Verificar que no exista ya este favorito
            favorito_existente