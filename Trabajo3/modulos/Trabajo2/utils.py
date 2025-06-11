"""
¡Aquí definimos funciones de utilidad para Remington Song API! 🛠️
Estas funciones nos ayudan a realizar tareas comunes de forma más sencilla.
"""
from datetime import datetime
import re

def validar_email(email):
    """
    Valida si un email tiene un formato correcto.
    """
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

def formatear_duracion(segundos):
    """
    Convierte segundos a formato mm:ss.
    """
    if not segundos:
        return "00:00"
    minutos = segundos // 60
    segundos_restantes = segundos % 60
    return f"{minutos:02d}:{segundos_restantes:02d}"

def validar_año(año):
    """
    Valida si un año es razonable para una canción.
    """
    if not año:
        return True  # El año es opcional
    año_actual = datetime.now().year
    return 1900 <= año <= año_actual

def limpiar_texto(texto):
    """
    Limpia un texto eliminando espacios extra y caracteres especiales.
    """
    if not texto:
        return ""
    texto = texto.strip()
    texto = re.sub(r'\\s+', ' ', texto)
    return texto

def generar_slug(texto):
    """
    Genera un slug a partir de un texto (útil para URLs amigables).
    """
    if not texto:
        return ""
    slug = texto.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug

def calcular_estadisticas_usuario(usuario_id):
    """
    Calcula estadísticas básicas de un usuario.
    """
    from remington_song.models import Usuario, Favorito, Cancion
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return None
    total_favoritos = len(usuario.favoritos)
    generos = {}
    for favorito in usuario.favoritos:
        if favorito.cancion.genero:
            genero = favorito.cancion.genero
            generos[genero] = generos.get(genero, 0) + 1
    genero_favorito = max(generos.items(), key=lambda x: x[1])[0] if generos else None
    return {
        'total_favoritos': total_favoritos,
        'genero_favorito': genero_favorito,
        'generos_estadisticas': generos
    }

def obtener_canciones_populares(limite=10):
    """
    Obtiene las canciones más populares basándose en la cantidad de favoritos.
    """
    from remington_song.models import Cancion, Favorito
    from remington_song.extensions import db
    from sqlalchemy import func
    canciones_populares = db.session.query(
        Cancion,
        func.count(Favorito.id).label('total_favoritos')
    ).outerjoin(Favorito).group_by(Cancion.id).order_by(
        func.count(Favorito.id).desc()
    ).limit(limite).all()
    return [
        {
            'cancion': cancion.to_dict(),
            'total_favoritos': total_favoritos
        }
        for cancion, total_favoritos in canciones_populares
    ]

def validar_datos_cancion(datos):
    """
    Valida los datos de una canción antes de guardarla.
    """
    errores = []
    if not datos.get('titulo'):
        errores.append("El título es requerido")
    elif len(datos['titulo']) > 100:
        errores.append("El título no puede tener más de 100 caracteres")
    if not datos.get('artista'):
        errores.append("El artista es requerido")
    elif len(datos['artista']) > 100:
        errores.append("El artista no puede tener más de 100 caracteres")
    if datos.get('album') and len(datos['album']) > 100:
        errores.append("El álbum no puede tener más de 100 caracteres")
    if datos.get('genero') and len(datos['genero']) > 50:
        errores.append("El género no puede tener más de 50 caracteres")
    if datos.get('duracion') and (datos['duracion'] < 0 or datos['duracion'] > 7200):
        errores.append("La duración debe estar entre 0 y 7200 segundos (2 horas)")
    if datos.get('año') and not validar_año(datos['año']):
        errores.append("El año debe estar entre 1900 y el año actual")
    return len(errores) == 0, errores

def validar_datos_usuario(datos):
    """
    Valida los datos de un usuario antes de guardarlo.
    """
    errores = []
    if not datos.get('nombre'):
        errores.append("El nombre es requerido")
    elif len(datos['nombre']) > 80:
        errores.append("El nombre no puede tener más de 80 caracteres")
    if not datos.get('correo'):
        errores.append("El correo es requerido")
    elif not validar_email(datos['correo']):
        errores.append("El formato del correo no es válido")
    elif len(datos['correo']) > 120:
        errores.append("El correo no puede tener más de 120 caracteres")
    if not datos.get('contraseña'):
        errores.append("La contraseña es requerida")
    elif len(datos['contraseña']) < 6:
        errores.append("La contraseña debe tener al menos 6 caracteres")
    return len(errores) == 0, errores

# Constantes útiles
GENEROS_MUSICALES = [
    'Rock', 'Pop', 'Hip Hop', 'R&B', 'Country', 'Jazz', 'Blues', 'Reggae',
    'Electronic', 'Classical', 'Folk', 'Punk', 'Metal', 'Alternative',
    'Indie', 'Funk', 'Soul', 'Gospel', 'Latin', 'World', 'Ambient',
    'House', 'Techno', 'Dubstep', 'Reggaeton', 'Salsa', 'Bachata',
    'Merengue', 'Cumbia', 'Vallenato', 'Tango'
]

DURACION_MAXIMA_CANCION = 7200  # 2 horas en segundos
DURACION_MINIMA_CANCION = 1     # 1 segundo

# Mensajes de respuesta comunes
MENSAJES = {
    'usuario_creado': '¡Usuario registrado exitosamente en Remington Song!',
    'usuario_actualizado': 'Usuario actualizado correctamente',
    'usuario_eliminado': 'Usuario eliminado de Remington Song',
    'cancion_creada': '¡Nueva canción agregada a Remington Song!',
    'cancion_actualizada': 'Canción actualizada correctamente',
    'cancion_eliminada': 'Canción eliminada de Remington Song',
    'favorito_agregado': '¡Canción agregada a tus favoritos!',
    'favorito_eliminado': 'Canción eliminada de tus favoritos',
    'login_exitoso': '¡Bienvenido a Remington Song!',
    'credenciales_invalidas': 'Credenciales inválidas',
    'token_invalido': 'Token de acceso inválido',
    'acceso_denegado': 'Acceso denegado'
}