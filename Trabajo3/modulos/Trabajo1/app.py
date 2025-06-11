"""
VideoStream API - Sistema de gestión de contenido multimedia
Desarrollado con Flask y arquitectura modular
"""

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from database import initialize_database
from api.endpoints import VideoResource, VideoListResource
from config import DevelopmentConfig
import logging

def create_app(config_class=DevelopmentConfig):
    """Factory pattern para crear la aplicación Flask"""

    # Inicializar Flask
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configurar CORS para permitir requests desde frontend
    CORS(app)

    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Inicializar base de datos
    initialize_database(app)

    # Configurar API REST
    api = Api(app, prefix='/api/v1')

    # Registrar endpoints
    api.add_resource(VideoResource, '/videos/<int:video_id>')
    api.add_resource(VideoListResource, '/videos')

    # Ruta de salud del sistema
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'VideoStream API'}, 200

    # Ruta principal con información de la API
    @app.route('/')
    def api_info():
        return {
            'service': 'VideoStream API',
            'version': '1.0.0',
            'description': 'API REST para gestión de contenido multimedia',
            'endpoints': {
                'videos': '/api/v1/videos',
                'video_detail': '/api/v1/videos/<id>',
                'health': '/health'
            }
        }

    return app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Iniciando VideoStream API...")
    print("📡 Servidor disponible en: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
